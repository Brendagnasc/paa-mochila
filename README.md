# Mochila 0-1 com duas restricoes (Projeto e Analise de Algoritmos - BCC241/UFOP)

Avaliacao empirica de tres estrategias para o problema da **mochila 0-1 com duas
restricoes**: maximizar o valor transportado numa mochila que suporta ao mesmo
tempo `W` quilos e `V` litros, escolhendo entre `n` itens (cada item entra
inteiro ou fica de fora). Cada item `i` tem peso `w_i`, volume `l_i` e valor `v_i`.

## Estrutura do projeto

```
.
├── algoritmos/        fontes C++ dos algoritmos (compilados aqui)
│   ├── mochila_pd.cpp          programacao dinamica
│   ├── mochila_bt.cpp          backtracking
│   ├── mochila_bb.cpp          branch-and-bound
│   └── mochila_pd_grande.cpp   PD com memoria otimizada (instancias grandes)
├── experimentos/      pipeline em Python
│   ├── gerar_instancias.py     gera instancias aleatorias
│   ├── rodar_experimentos.py   roda e mede; gera resultados/tempos.csv
│   ├── analise_estatistica.py  teste de Friedman por combinacao
│   ├── gerar_graficos.py       graficos de tempo
│   └── teste_random.py         teste de corretude e tempo
├── relatorio/
│   └── build_relatorio.js      gera relatorio_mochila.docx
├── resultados/        saidas geradas (fica no .gitignore)
├── exemplo.txt
├── Makefile
└── README.md
```

## Algoritmos

| Arquivo | Estrategia | Tempo (pior caso) | Espaco |
|---|---|---|---|
| `mochila_pd.cpp` | Programacao dinamica | O(n . W . V) | O(n . W . V) |
| `mochila_bt.cpp` | Backtracking (poda por viabilidade) | O(2^n) | O(n) |
| `mochila_bb.cpp` | Branch-and-bound (limite por relaxacao do peso) | O(2^n) | O(n) |
| `mochila_pd_grande.cpp` | PD com vetor de rolagem | O(n . W . V) | O(W . V) |

As implementacoes sao exatas e produzem o mesmo lucro maximo. A `mochila_pd_grande`
serve para instancias grandes, onde a tabela 3D da PD padrao excederia a memoria.
Os algoritmos exponenciais (BT e BB) so sao viaveis para poucas dezenas de itens.

## Comandos (Makefile)

Todos os comandos sao rodados na raiz do projeto.

```
make                 compila os quatro programas C++
make teste           teste de corretude e tempo
make experimentos    roda os experimentos (gera resultados/tempos.csv)
make estatistica     teste de Friedman por combinacao
make graficos        gera os graficos
make relatorio       gera o relatorio em Word
make limpar          apaga binarios e saidas geradas
```

Para passar parametros aos scripts, use `ARGS`. Exemplos:

```
make teste ARGS="-i 2000 --estimar"
make experimentos ARGS="--estimar -i 5"
make experimentos ARGS="--rapido"
```

Os scripts tambem podem ser chamados direto, de qualquer pasta, por exemplo
`python3 experimentos/teste_random.py -n 200 --sem-bt`.

## Ordem do pipeline

1. `make experimentos`  -> gera `resultados/tempos.csv`
2. `make estatistica`   -> gera `resultados/estatistica.csv`
3. `make graficos`      -> gera os PNGs em `resultados/`
4. `make relatorio`     -> gera `relatorio_mochila.docx`

## Formato de entrada e saida

Entrada (arquivo texto):
- 1a linha: `W  V`
- demais linhas: `peso  volume  valor` (separados por espaco ou tabulacao)

Saida: lucro maximo, itens na mochila (indices na ordem de entrada) e tempo de
execucao (medido apenas em torno do nucleo do algoritmo).

Exemplo de uso direto de um programa:

```bash
./algoritmos/mochila_pd exemplo.txt
```

## Parametros dos testes

`teste_random.py` (e `make teste ARGS=...`):
- `-i N`  quantidade de instancias (padrao 400)
- `-n N`  numero maximo de itens por instancia (padrao 14)
- `-c N`  capacidade maxima (padrao 40)
- `--sem-bt`  nao testa o backtracking (use para n grande)
- `--com-pd-grande`  inclui a PD otimizada
- `--estimar`  mostra a estimativa antes da bateria real

`rodar_experimentos.py` (e `make experimentos ARGS=...`):
- `-i N`  instancias por combinacao (padrao 10, ou 3 com `--rapido`)
- `--rapido`  grade pequena para validar o pipeline
- `--estimar`  mostra a estimativa antes da rodada completa

## Dependencias

- Compilador C++17 (g++) e make
- Python 3 com `scipy` e `matplotlib`: `pip install scipy matplotlib`
- Node.js com `docx`: `npm install -g docx`

## Autores

Grupo de Projeto e Analise de Algoritmos (BCC241) - UFOP.
