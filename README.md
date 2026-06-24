# Mochila 0-1 com duas restricoes (Projeto e Analise de Algoritmos - BCC241/UFOP)

Avaliacao empirica de tres estrategias para o problema da **mochila 0-1 com duas
restricoes**: maximizar o valor transportado numa mochila que suporta ao mesmo
tempo `W` quilos e `V` litros, escolhendo entre `n` itens (cada item entra
inteiro ou fica de fora). Cada item `i` tem peso `w_i`, volume `l_i` e valor `v_i`.

O repositorio contem as implementacoes dos algoritmos, todo o pipeline de
avaliacao experimental (geracao de instancias, execucao, estatistica e graficos)
e o gerador do relatorio final.

## Estrutura do projeto

Algoritmos (C++17):
- `mochila_pd.cpp` - programacao dinamica
- `mochila_bt.cpp` - backtracking
- `mochila_bb.cpp` - branch-and-bound
- `mochila_pd_grande.cpp` - programacao dinamica com memoria otimizada (instancias grandes)

Pipeline experimental (Python 3):
- `gerar_instancias.py` - gera instancias aleatorias no formato de entrada
- `rodar_experimentos.py` - gera, executa e mede; produz `resultados/tempos.csv`
- `analise_estatistica.py` - teste de Friedman por combinacao; produz `resultados/estatistica.csv`
- `gerar_graficos.py` - graficos de tempo x n e tempo x capacidade
- `teste_random.py` - teste de corretude (compara os tres algoritmos)

Relatorio:
- `build_relatorio.js` - gera `relatorio_mochila.docx` (Node.js)

## Implementacoes

| Arquivo | Estrategia | Tempo (pior caso) | Espaco |
|---|---|---|---|
| `mochila_pd.cpp` | Programacao dinamica | O(n . W . V) | O(n . W . V) |
| `mochila_bt.cpp` | Backtracking (poda por viabilidade) | O(2^n) | O(n) |
| `mochila_bb.cpp` | Branch-and-bound (limite por relaxacao fracionaria do peso) | O(2^n) | O(n) |
| `mochila_pd_grande.cpp` | Programacao dinamica (vetor de rolagem) | O(n . W . V) | O(W . V) |

As implementacoes sao exatas e produzem sempre o mesmo lucro maximo. A versao
`mochila_pd_grande` deve ser usada em instancias grandes (muitos itens ou
capacidades altas), em que a tabela 3D completa da PD padrao excederia a memoria.
Os algoritmos exponenciais (BT e BB) so sao viaveis para poucas dezenas de itens.

## Formato de entrada e saida

Entrada (arquivo texto):
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

Saida: lucro maximo, itens na mochila (indices na ordem de entrada) e tempo de
execucao (medido apenas em torno do nucleo do algoritmo, sem a leitura do arquivo).

## Como compilar

```bash
make
```

Gera os executaveis `mochila_pd`, `mochila_bt`, `mochila_bb` e `mochila_pd_grande`.
Use sempre a otimizacao `-O2` (ja configurada no Makefile); sem ela, a PD com
muitos itens fica varias vezes mais lenta.

## Como executar

```bash
./mochila_pd exemplo.txt
./mochila_bt exemplo.txt
./mochila_bb exemplo.txt
./mochila_pd_grande exemplo.txt
```

## Pipeline de experimentos

1. Executar os experimentos (gera `resultados/tempos.csv`):

```bash
python3 rodar_experimentos.py            # grade completa
python3 rodar_experimentos.py --rapido   # grade pequena, so para validar
```

2. Analise estatistica (gera `resultados/estatistica.csv`):

```bash
python3 analise_estatistica.py
```

3. Graficos (gera `resultados/tempo_vs_n.png` e `resultados/tempo_vs_capacidade.png`):

```bash
python3 gerar_graficos.py
```

As combinacoes de `n`, `W` e `V` ficam no topo do `rodar_experimentos.py`. Se voce
alterar a grade, ajuste tambem as constantes `FATOR_CAP` e `N_FIXO` no
`gerar_graficos.py` para os graficos continuarem coerentes.

## Relatorio

```bash
node build_relatorio.js
```

Gera `relatorio_mochila.docx`, ja com a estrutura preenchida e os graficos
embutidos a partir de `resultados/`. Rode os graficos antes.

## Teste de corretude

```bash
python3 teste_random.py
```

Compara as tres implementacoes em 400 instancias aleatorias e confirma que todas
chegam ao mesmo otimo.

## Dependencias

- Compilador C++17 (g++) e make
- Python 3 com `scipy` (estatistica) e `matplotlib` (graficos):
  `pip install scipy matplotlib`
- Node.js com o pacote `docx` (relatorio): `npm install -g docx`

## Autores

Grupo de Projeto e Analise de Algoritmos (BCC241) - UFOP.
