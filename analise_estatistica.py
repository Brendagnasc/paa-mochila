#!/usr/bin/env python3
# analise_estatistica.py
# Le resultados/tempos.csv e, para CADA combinacao (n, W, V), aplica um teste
# estatistico para verificar se houve EMPATE ESTATISTICO entre os tres
# algoritmos.
#
# Metodo:
#   - Teste de Friedman (nao parametrico, amostras pareadas): as 10 instancias
#     foram resolvidas pelos tres algoritmos, entao as medidas sao pareadas.
#     O teste responde "ha diferenca significativa entre os tres tempos?".
#       p <  alpha  -> ha diferenca (NAO e empate geral)
#       p >= alpha  -> empate estatistico entre os tres
#   - Pos-teste (se Friedman for significativo): Wilcoxon dos postos sinalizados
#     par a par (PD-BT, PD-BB, BT-BB), com correcao de Bonferroni (alpha/3),
#     para identificar QUAIS pares diferem e quais empatam.
#
# Saida: tabela no terminal + resultados/estatistica.csv
#
# Requer: scipy  (pip install scipy)

import csv
import os
from collections import defaultdict
from itertools import combinations

from scipy.stats import friedmanchisquare, wilcoxon

ALPHA = 0.05
ARQUIVO_CSV = os.path.join("resultados", "tempos.csv")
ARQUIVO_SAIDA = os.path.join("resultados", "estatistica.csv")
ALGS = ["pd", "bt", "bb"]
NOME = {"pd": "PD", "bt": "BT", "bb": "BB"}


def ler_dados(caminho):
    """Retorna {(n,W,V): {instancia: {alg: (tempo, status)}}}."""
    dados = defaultdict(lambda: defaultdict(dict))
    with open(caminho, newline="") as f:
        for r in csv.DictReader(f):
            comb = (int(r["n"]), int(r["W"]), int(r["V"]))
            inst = int(r["instancia"])
            tempo = float(r["tempo_s"]) if r["tempo_s"] else None
            dados[comb][inst][r["algoritmo"]] = (tempo, r["status"])
    return dados


def tempos_pareados(instancias):
    """Para uma combinacao, devolve as listas de tempos alinhadas por instancia,
    usando so as instancias em que TODOS os algoritmos rodaram com sucesso."""
    series = {a: [] for a in ALGS}
    timeouts = {a: 0 for a in ALGS}
    for inst in sorted(instancias):
        medidas = instancias[inst]
        for a in ALGS:
            if a in medidas and medidas[a][1] == "timeout":
                timeouts[a] += 1
        if all(a in medidas and medidas[a][1] == "ok" and medidas[a][0] is not None
               for a in ALGS):
            for a in ALGS:
                series[a].append(medidas[a][0])
    return series, timeouts


def media(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def ranking(series):
    """Ordena os algoritmos pelo tempo medio (menor primeiro)."""
    return sorted(ALGS, key=lambda a: media(series[a]))


def analisar_combinacao(comb, instancias):
    series, timeouts = tempos_pareados(instancias)
    n_amostras = len(series["pd"])
    linha = {
        "n": comb[0], "W": comb[1], "V": comb[2],
        "n_amostras": n_amostras,
        "media_pd": f"{media(series['pd']):.6f}",
        "media_bt": f"{media(series['bt']):.6f}",
        "media_bb": f"{media(series['bb']):.6f}",
        "timeouts": ";".join(f"{NOME[a]}={timeouts[a]}" for a in ALGS if timeouts[a]),
        "friedman_p": "", "conclusao": "", "ranking": "", "pares_empatados": "",
    }

    if n_amostras < 3:
        linha["conclusao"] = "amostras insuficientes (timeouts)"
        return linha

    # Teste omnibus de Friedman.
    try:
        stat, p = friedmanchisquare(series["pd"], series["bt"], series["bb"])
    except ValueError:
        # ocorre quando os tempos sao identicos (sem variacao)
        linha["conclusao"] = "empate estatistico (sem variacao)"
        linha["ranking"] = " < ".join(NOME[a] for a in ranking(series))
        return linha

    linha["friedman_p"] = f"{p:.4g}"
    ordem = ranking(series)
    linha["ranking"] = " < ".join(NOME[a] for a in ordem)

    if p >= ALPHA:
        linha["conclusao"] = "empate estatistico entre os tres"
        linha["pares_empatados"] = "todos"
        return linha

    # Pos-teste par a par (Bonferroni).
    linha["conclusao"] = "ha diferenca significativa"
    alpha_aj = ALPHA / 3
    empatados = []
    for a, b in combinations(ALGS, 2):
        try:
            _, pp = wilcoxon(series[a], series[b])
        except ValueError:
            pp = 1.0  # diferencas todas nulas -> empate
        if pp >= alpha_aj:
            empatados.append(f"{NOME[a]}={NOME[b]}")
    linha["pares_empatados"] = ", ".join(empatados) if empatados else "nenhum"
    return linha


def main():
    if not os.path.exists(ARQUIVO_CSV):
        print(f"Arquivo nao encontrado: {ARQUIVO_CSV}")
        print("Rode antes:  python3 rodar_experimentos.py")
        return

    dados = ler_dados(ARQUIVO_CSV)
    linhas = [analisar_combinacao(c, dados[c]) for c in sorted(dados)]

    # Impressao no terminal.
    print(f"\nTeste de empate estatistico por combinacao (alpha = {ALPHA})\n")
    cab = f"{'n':>3} {'W':>4} {'V':>4} | {'PD(s)':>9} {'BT(s)':>9} {'BB(s)':>9} | {'Friedman p':>10} | conclusao"
    print(cab)
    print("-" * len(cab))
    for L in linhas:
        extra = ""
        if L["pares_empatados"] and L["pares_empatados"] not in ("todos", ""):
            extra = f"  [empatam: {L['pares_empatados']}]"
        if L["timeouts"]:
            extra += f"  (timeouts: {L['timeouts']})"
        print(f"{L['n']:>3} {L['W']:>4} {L['V']:>4} | "
              f"{L['media_pd']:>9} {L['media_bt']:>9} {L['media_bb']:>9} | "
              f"{L['friedman_p']:>10} | {L['conclusao']}{extra}")

    campos = ["n", "W", "V", "n_amostras", "media_pd", "media_bt", "media_bb",
              "friedman_p", "conclusao", "ranking", "pares_empatados", "timeouts"]
    with open(ARQUIVO_SAIDA, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)
    print(f"\nResumo salvo em '{ARQUIVO_SAIDA}'.")


if __name__ == "__main__":
    main()
