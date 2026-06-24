#!/usr/bin/env python3
# gerar_instancias.py
# Gera instancias aleatorias da mochila 0-1 com duas restricoes, no formato
# esperado pelos programas C++:
#   1a linha:  W  V
#   demais:    peso  volume  valor   (separados por tabulacao)
#
# Os atributos dos itens (peso, volume, valor) sao sorteados de faixas fixas,
# enquanto W e V (capacidades) sao os parametros que variamos nos experimentos.
# A semente e deterministica por combinacao, entao as instancias sao sempre as
# mesmas (reprodutibilidade).

import os
import random

# Faixas dos atributos dos itens (fixas em todos os experimentos).
PESO_MAX = 10
VOLUME_MAX = 10
VALOR_MAX = 100


def gerar_instancia(n, W, V, rng):
    """Retorna o texto de uma instancia com n itens e capacidades W, V."""
    linhas = [f"{W} {V}"]
    for _ in range(n):
        peso = rng.randint(1, PESO_MAX)
        volume = rng.randint(1, VOLUME_MAX)
        valor = rng.randint(1, VALOR_MAX)
        linhas.append(f"{peso}\t{volume}\t{valor}")
    return "\n".join(linhas) + "\n"


def semente(seed_base, n, W, V, i):
    """Semente inteira deterministica para a i-esima instancia da combinacao."""
    return (seed_base * 1000003 + n * 10007 + W * 101 + V) * 100 + i


def gerar_para_combinacao(n, W, V, qtd, pasta, seed_base):
    """Gera 'qtd' instancias para a combinacao (n, W, V) e devolve os caminhos."""
    os.makedirs(pasta, exist_ok=True)
    caminhos = []
    for i in range(1, qtd + 1):
        rng = random.Random(semente(seed_base, n, W, V, i))
        conteudo = gerar_instancia(n, W, V, rng)
        caminho = os.path.join(pasta, f"n{n}_W{W}_V{V}_i{i}.txt")
        with open(caminho, "w") as f:
            f.write(conteudo)
        caminhos.append(caminho)
    return caminhos


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Gera instancias da mochila 0-1 com duas restricoes.")
    ap.add_argument("-n", type=int, required=True, help="quantidade de itens")
    ap.add_argument("-W", type=int, required=True, help="capacidade de peso")
    ap.add_argument("-V", type=int, required=True, help="capacidade de volume")
    ap.add_argument("--qtd", type=int, default=10, help="quantidade de instancias (padrao 10)")
    ap.add_argument("--pasta", default="instancias", help="pasta de saida")
    ap.add_argument("--seed", type=int, default=12345, help="semente base")
    args = ap.parse_args()

    caminhos = gerar_para_combinacao(args.n, args.W, args.V, args.qtd, args.pasta, args.seed)
    print(f"{len(caminhos)} instancias geradas em '{args.pasta}/'")
