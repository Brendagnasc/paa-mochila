#!/usr/bin/env python3
# rodar_experimentos.py
# Orquestra a avaliacao empirica:
#   1. compila os tres programas (make)
#   2. para cada combinacao (n, W, V), gera 'QTD_INSTANCIAS' instancias
#   3. roda os tres algoritmos sobre cada instancia, mede o tempo e o lucro
#   4. salva tudo em resultados/tempos.csv
#
# O tempo registrado e o que o proprio programa reporta (medido so em volta do
# nucleo do algoritmo, sem a leitura do arquivo). Combinacoes em que um algoritmo
# estoura o limite de tempo sao marcadas como 'timeout' (isso e um resultado: o
# algoritmo se tornou inviavel naquele tamanho).
#
# Uso:
#   python3 rodar_experimentos.py            # grade completa (pode demorar)
#   python3 rodar_experimentos.py --rapido   # grade pequena, so para validar

import argparse
import csv
import os
import re
import subprocess
import sys

from gerar_instancias import gerar_para_combinacao

# ---------------------------------------------------------------------------
# Configuracao dos experimentos (ajuste a vontade)
# ---------------------------------------------------------------------------
QTD_INSTANCIAS = 10        # instancias por combinacao (o enunciado pede 10)
SEED_BASE = 12345          # semente base para reprodutibilidade
TIMEOUT_S = 60             # limite de tempo por execucao (segundos)
PASTA_INST = "instancias"
PASTA_RES = "resultados"
ARQUIVO_CSV = os.path.join(PASTA_RES, "tempos.csv")

ALGORITMOS = [
    ("pd", "./mochila_pd"),
    ("bt", "./mochila_bt"),
    ("bb", "./mochila_bb"),
]

# Varredura 1 - EFEITO DE n: capacidade cresce com n (regime dificil, ~metade
# dos itens cabe), para evidenciar a explosao exponencial de BT e B&B contra o
# crescimento polinomial da PD. Peso/volume medios ~5.5, entao W=V~=3*n deixa
# aproximadamente metade dos itens cabendo.
def grade_efeito_n():
    combos = []
    for n in [10, 15, 20, 25, 30]:
        cap = 3 * n
        combos.append((n, cap, cap))
    return combos

# Varredura 2 - EFEITO DA CAPACIDADE: n fixo, variando W e V, para ver a PD
# crescer com W*V.
def grade_efeito_capacidade():
    combos = []
    for cap in [25, 50, 75, 100, 125]:
        combos.append((20, cap, cap))
    return combos

# Grade reduzida, so para validar o pipeline rapidamente.
def grade_rapida():
    return [(10, 30, 30), (14, 42, 42), (18, 54, 54), (15, 30, 30), (15, 60, 60)]
# ---------------------------------------------------------------------------

RE_LUCRO = re.compile(r"Lucro maximo:\s*(\d+)")
RE_TEMPO = re.compile(r"Tempo de execucao:\s*([0-9.eE+-]+)")


def compilar():
    print("Compilando (make)...")
    r = subprocess.run(["make"], capture_output=True, text=True)
    if r.returncode != 0:
        print("Falha ao compilar. Saida do make:\n" + r.stderr)
        sys.exit(1)
    for _, prog in ALGORITMOS:
        if not os.path.exists(prog):
            print(f"Executavel nao encontrado: {prog}")
            sys.exit(1)


def rodar(prog, arquivo):
    """Roda um programa numa instancia. Retorna (lucro, tempo, status)."""
    try:
        r = subprocess.run([prog, arquivo], capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None, None, "timeout"
    ml = RE_LUCRO.search(r.stdout)
    mt = RE_TEMPO.search(r.stdout)
    lucro = int(ml.group(1)) if ml else None
    tempo = float(mt.group(1)) if mt else None
    return lucro, tempo, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true", help="grade pequena para validar o pipeline")
    args = ap.parse_args()

    compilar()

    if args.rapido:
        combos = grade_rapida()
        qtd = 3
    else:
        combos = grade_efeito_n() + grade_efeito_capacidade()
        # remove combinacoes repetidas preservando a ordem
        vistos = set()
        combos = [c for c in combos if not (c in vistos or vistos.add(c))]
        qtd = QTD_INSTANCIAS

    os.makedirs(PASTA_RES, exist_ok=True)
    linhas_csv = []
    print(f"\n{len(combos)} combinacoes, {qtd} instancias cada.\n")

    for (n, W, V) in combos:
        arquivos = gerar_para_combinacao(n, W, V, qtd, PASTA_INST, SEED_BASE)
        # acumula tempos por algoritmo para o resumo
        tempos = {nome: [] for nome, _ in ALGORITMOS}
        for inst_idx, arquivo in enumerate(arquivos, start=1):
            lucros = {}
            for nome, prog in ALGORITMOS:
                lucro, tempo, status = rodar(prog, arquivo)
                lucros[nome] = lucro
                if status == "ok" and tempo is not None:
                    tempos[nome].append(tempo)
                linhas_csv.append({
                    "n": n, "W": W, "V": V, "instancia": inst_idx,
                    "algoritmo": nome, "lucro": lucro if lucro is not None else "",
                    "tempo_s": f"{tempo:.6f}" if tempo is not None else "",
                    "status": status,
                })
            # checagem de corretude: os tres devem concordar no lucro otimo
            validos = [v for v in lucros.values() if v is not None]
            if len(set(validos)) > 1:
                print(f"  [ATENCAO] lucros divergentes em n{n}_W{W}_V{V}_i{inst_idx}: {lucros}")

        def media(xs):
            return sum(xs) / len(xs) if xs else float("nan")
        print(f"n={n:>3} W={W:>3} V={V:>3} | "
              f"PD={media(tempos['pd']):.6f}s  "
              f"BT={media(tempos['bt']):.6f}s  "
              f"BB={media(tempos['bb']):.6f}s")

    with open(ARQUIVO_CSV, "w", newline="") as f:
        campos = ["n", "W", "V", "instancia", "algoritmo", "lucro", "tempo_s", "status"]
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas_csv)

    print(f"\nResultados salvos em '{ARQUIVO_CSV}' ({len(linhas_csv)} linhas).")


if __name__ == "__main__":
    main()
