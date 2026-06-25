#!/usr/bin/env python3
# teste_random.py
# Testa a CORRETUDE dos algoritmos da mochila (todos chegam ao mesmo lucro otimo)
# e mostra o TEMPO de execucao medio e total de cada algoritmo.
#
# Parametros por linha de comando (todos opcionais):
#   -i / --instancias    quantidade de instancias testadas (padrao 400)
#   -n / --n-max         numero MAXIMO de itens por instancia (padrao 14)
#   -c / --cap-max       capacidade maxima de peso e volume (padrao 40)
#   --sem-bt             nao testa o backtracking (use para n grande)
#   --com-pd-grande      inclui a PD otimizada (mochila_pd_grande)
#   --estimar            mostra a estimativa (a partir de uma amostra) antes da bateria real
#   --seed               semente do gerador (padrao 42)
#
# Exemplos:
#   python3 teste_random.py                      # so os valores reais
#   python3 teste_random.py -i 2000 --estimar    # estimativa + valores reais
#   python3 teste_random.py -n 200 --sem-bt      # 200 itens, sem o backtracking

import argparse
import random
import re
import subprocess
import time

RE_LUCRO = re.compile(r"Lucro maximo:\s*(\d+)")
RE_TEMPO = re.compile(r"Tempo de execucao:\s*([0-9.eE+-]+)")


def fmt(segundos):
    """Formata uma duracao de forma legivel."""
    if segundos < 90:
        return f"{segundos:.1f}s"
    minutos = segundos / 60
    if minutos < 90:
        return f"{minutos:.1f} min"
    return f"{minutos / 60:.2f} h"


def rodar(prog, entrada):
    """Roda um programa e devolve (lucro, tempo_em_segundos)."""
    p = subprocess.run([prog], input=entrada, capture_output=True, text=True)
    ml = RE_LUCRO.search(p.stdout)
    mt = RE_TEMPO.search(p.stdout)
    lucro = int(ml.group(1)) if ml else None
    tempo = float(mt.group(1)) if mt else None
    return lucro, tempo


def gerar_entrada(n_max, cap_max):
    """Gera o texto de uma instancia aleatoria."""
    n = random.randint(1, n_max)
    W = random.randint(1, cap_max)
    V = random.randint(1, cap_max)
    linhas = [f"{W} {V}"]
    for _ in range(n):
        w = random.randint(1, 20)
        l = random.randint(1, 20)
        val = random.randint(1, 50)
        linhas.append(f"{w}\t{l}\t{val}")
    return "\n".join(linhas) + "\n"


def estimar(algos, args):
    """Roda uma amostra e imprime a estimativa de tempo, projetando para o total."""
    amostra = min(args.instancias, 30)
    print(f"Rodando amostra de {amostra} instancias para estimar...\n")
    random.seed(args.seed)
    tempos = {nome: [] for nome, _ in algos}
    inicio = time.perf_counter()
    for _ in range(amostra):
        entrada = gerar_entrada(args.n_max, args.cap_max)
        for nome, prog in algos:
            _, tempo = rodar(prog, entrada)
            if tempo is not None:
                tempos[nome].append(tempo)
    proj_wall = (time.perf_counter() - inicio) / amostra * args.instancias

    print(f"ESTIMATIVA para {args.instancias} instancias (amostra de {amostra}, "
          f"itens ate {args.n_max}):")
    print(f"  {'algoritmo':<10} {'medio (s)':>14} {'total estimado (s)':>20}")
    for nome, _ in algos:
        ts = tempos[nome]
        med = sum(ts) / len(ts) if ts else 0.0
        print(f"  {nome:<10} {med:>14.6f} {med * args.instancias:>20.6f}")
    print(f"  Tempo total estimado (relogio): ~{fmt(proj_wall)}\n")


def rodar_bateria(algos, args):
    """Roda a bateria completa, valida a corretude e imprime os tempos reais."""
    random.seed(args.seed)
    falhas = 0
    tempos = {nome: [] for nome, _ in algos}
    inicio = time.perf_counter()
    for _ in range(args.instancias):
        entrada = gerar_entrada(args.n_max, args.cap_max)
        lucros = {}
        for nome, prog in algos:
            lucro, tempo = rodar(prog, entrada)
            lucros[nome] = lucro
            if tempo is not None:
                tempos[nome].append(tempo)
        if len(set(lucros.values())) > 1:
            falhas += 1
            print("DIVERGENCIA:", lucros)
            print(entrada)
            if falhas > 5:
                break
    elapsed = time.perf_counter() - inicio

    nomes = ", ".join(nome for nome, _ in algos)
    print(f"Testes: {args.instancias} | itens ate {args.n_max} | "
          f"algoritmos: {nomes} | falhas: {falhas}")
    print("OK - todos concordam no otimo" if falhas == 0
          else "ATENCAO: ha divergencias")

    print("\nTempo de execucao por algoritmo (apenas o nucleo do algoritmo):")
    print(f"  {'algoritmo':<10} {'medio (s)':>14} {'total (s)':>14}")
    for nome, _ in algos:
        ts = tempos[nome]
        med = sum(ts) / len(ts) if ts else 0.0
        print(f"  {nome:<10} {med:>14.6f} {sum(ts):>14.6f}")
    print(f"\nTempo total da bateria (relogio): {fmt(elapsed)}")


def main():
    ap = argparse.ArgumentParser(
        description="Testa a corretude e mede o tempo dos algoritmos da mochila.")
    ap.add_argument("-i", "--instancias", type=int, default=400,
                    help="quantidade de instancias (padrao 400)")
    ap.add_argument("-n", "--n-max", type=int, default=14,
                    help="numero maximo de itens por instancia (padrao 14)")
    ap.add_argument("-c", "--cap-max", type=int, default=40,
                    help="capacidade maxima de peso e volume (padrao 40)")
    ap.add_argument("--sem-bt", action="store_true",
                    help="nao testa o backtracking (recomendado para n grande)")
    ap.add_argument("--com-pd-grande", action="store_true",
                    help="inclui a PD otimizada (mochila_pd_grande) na comparacao")
    ap.add_argument("--estimar", action="store_true",
                    help="mostra a estimativa (a partir de uma amostra) antes da bateria real")
    ap.add_argument("--seed", type=int, default=42, help="semente (padrao 42)")
    args = ap.parse_args()

    algos = [("PD", "./mochila_pd")]
    if not args.sem_bt:
        algos.append(("BT", "./mochila_bt"))
    algos.append(("BB", "./mochila_bb"))
    if args.com_pd_grande:
        algos.append(("PDG", "./mochila_pd_grande"))

    if not args.sem_bt and args.n_max > 20:
        print(f"[aviso] n-max={args.n_max} com backtracking pode ser MUITO lento, "
              f"pois ele e O(2^n). Considere usar --sem-bt.\n")

    if args.estimar:
        estimar(algos, args)
    rodar_bateria(algos, args)


if __name__ == "__main__":
    main()
