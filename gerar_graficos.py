#!/usr/bin/env python3
# gerar_graficos.py
# Le resultados/tempos.csv e gera dois graficos do tempo de execucao:
#   1) tempo x quantidade de itens (n), no regime dificil (W=V=FATOR_CAP*n)
#   2) tempo x capacidade (W=V), com n fixo (N_FIXO)
#
# O eixo do tempo fica em escala logaritmica: e o que deixa visivel, na mesma
# figura, a curva exponencial do backtracking ao lado do crescimento polinomial
# da PD e do branch-and-bound. As barras de erro mostram o desvio padrao das 10
# instancias.
#
# Requer: matplotlib  (pip install matplotlib)

import csv
import os
from collections import defaultdict
from statistics import mean, pstdev

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Devem casar com a configuracao do rodar_experimentos.py
FATOR_CAP = 3     # no efeito de n, capacidade = FATOR_CAP * n
N_FIXO = 20       # no efeito da capacidade, n fixo

ARQUIVO_CSV = os.path.join("resultados", "tempos.csv")
PASTA_RES = "resultados"
ALGS = ["pd", "bt", "bb"]
NOME = {"pd": "Programacao dinamica", "bt": "Backtracking", "bb": "Branch-and-bound"}
ESTILO = {"pd": ("o", "#1f77b4"), "bt": ("s", "#d62728"), "bb": ("^", "#2ca02c")}


def ler_tempos(caminho):
    """Retorna {(n,W,V): {alg: [tempos_ok]}}."""
    d = defaultdict(lambda: defaultdict(list))
    with open(caminho, newline="") as f:
        for r in csv.DictReader(f):
            if r["status"] == "ok" and r["tempo_s"]:
                comb = (int(r["n"]), int(r["W"]), int(r["V"]))
                d[comb][r["algoritmo"]].append(float(r["tempo_s"]))
    return d


def plotar(dados, combos, xs, titulo, xlabel, arquivo):
    plt.figure(figsize=(8, 5))
    for a in ALGS:
        X, Y, E = [], [], []
        for (comb, x) in zip(combos, xs):
            tempos = dados.get(comb, {}).get(a, [])
            if tempos:
                X.append(x)
                Y.append(mean(tempos))
                E.append(pstdev(tempos) if len(tempos) > 1 else 0.0)
        if X:
            marcador, cor = ESTILO[a]
            plt.errorbar(X, Y, yerr=E, marker=marcador, color=cor, capsize=3,
                         linewidth=1.8, markersize=6, label=NOME[a])
    plt.yscale("log")
    plt.xlabel(xlabel)
    plt.ylabel("Tempo de execucao (s) - escala log")
    plt.title(titulo)
    plt.grid(True, which="both", linestyle=":", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    caminho = os.path.join(PASTA_RES, arquivo)
    plt.savefig(caminho, dpi=150)
    plt.close()
    return caminho


def main():
    if not os.path.exists(ARQUIVO_CSV):
        print(f"Arquivo nao encontrado: {ARQUIVO_CSV}")
        print("Rode antes:  python3 rodar_experimentos.py")
        return

    dados = ler_tempos(ARQUIVO_CSV)
    os.makedirs(PASTA_RES, exist_ok=True)
    gerados = []

    # Grafico 1: efeito de n (W = V = FATOR_CAP * n)
    combos_n = sorted(c for c in dados if c[1] == c[2] == FATOR_CAP * c[0])
    if combos_n:
        xs = [c[0] for c in combos_n]
        gerados.append(plotar(
            dados, combos_n, xs,
            f"Tempo x quantidade de itens (W = V = {FATOR_CAP}n)",
            "Quantidade de itens (n)", "tempo_vs_n.png"))
    else:
        print("Sem combinacoes para o grafico de efeito de n "
              f"(esperado W=V={FATOR_CAP}*n).")

    # Grafico 2: efeito da capacidade (n fixo)
    combos_cap = sorted((c for c in dados if c[0] == N_FIXO and c[1] == c[2]),
                        key=lambda c: c[1])
    if combos_cap:
        xs = [c[1] for c in combos_cap]
        gerados.append(plotar(
            dados, combos_cap, xs,
            f"Tempo x capacidade (n = {N_FIXO}, W = V)",
            "Capacidade (W = V)", "tempo_vs_capacidade.png"))
    else:
        print(f"Sem combinacoes para o grafico de capacidade (esperado n={N_FIXO}).")

    for g in gerados:
        print(f"Grafico salvo: {g}")


if __name__ == "__main__":
    main()
