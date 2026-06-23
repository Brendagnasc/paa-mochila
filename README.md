# Mochila 0-1 com duas restricoes (Projeto e Analise de Algoritmos - BCC241/UFOP)

Avaliacao empirica de tres estrategias para o problema da **mochila 0-1 com duas
restricoes**: maximizar o valor transportado numa mochila que suporta ao mesmo
tempo `W` quilos e `V` litros, escolhendo entre `n` itens (cada item entra
inteiro ou fica de fora). Cada item `i` tem peso `w_i`, volume `l_i` e valor `v_i`.

## Implementacoes

| Arquivo | Estrategia | Tempo (pior caso) | Espaco |
|---|---|---|---|
| `mochila_pd.cpp` | Programacao dinamica | O(n . W . V) | O(n . W . V) |
| `mochila_bt.cpp` | Backtracking (poda por viabilidade) | O(2^n) | O(n) |
| `mochila_bb.cpp` | Branch-and-bound (limite por relaxacao fracionaria do peso) | O(2^n) | O(n) |

As tres implementacoes sao exatas e produzem sempre o mesmo lucro maximo.

## Formato de entrada

Arquivo texto:
- 1a linha: `W  V`
- demais linhas: `peso  volume  valor` (separados por espaco ou tabulacao)

Exemplo (`exemplo.txt`):

```
10	9
6	3	10
3	4	14
4	2	16
2	5	9
```

## Como compilar

```bash
make
```

Gera os executaveis `mochila_pd`, `mochila_bt` e `mochila_bb`.

## Como executar

```bash
./mochila_pd exemplo.txt
./mochila_bt exemplo.txt
./mochila_bb exemplo.txt
```

Saida: lucro maximo, itens na mochila (indices na ordem de entrada) e tempo de
execucao (medido apenas em volta do nucleo do algoritmo, sem a leitura do arquivo).

## Teste de corretude

```bash
python3 teste_random.py
```

Compara as tres implementacoes em 400 instancias aleatorias e confirma que todas
chegam ao mesmo otimo.

## Autores

Grupo de Projeto e Analise de Algoritmos (BCC241) - UFOP.
