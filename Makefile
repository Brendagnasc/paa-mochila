# Makefile central do projeto: compila os algoritmos e roda o pipeline.
#
# Alvos principais:
#   make                 compila os quatro programas C++
#   make teste           teste de corretude e tempo
#   make experimentos    roda os experimentos (gera resultados/tempos.csv)
#   make estatistica     teste de Friedman por combinacao
#   make graficos        gera os graficos
#   make relatorio       gera o relatorio em Word
#   make limpar          apaga binarios e saidas geradas
#
# Para passar parametros aos scripts, use ARGS, por exemplo:
#   make teste ARGS="-i 2000 --estimar"
#   make experimentos ARGS="--estimar -i 5"

CXX      = g++
CXXFLAGS = -std=c++17 -O2 -Wall
ALG      = algoritmos
PY       = python3

BINS = $(ALG)/mochila_pd $(ALG)/mochila_bt $(ALG)/mochila_bb $(ALG)/mochila_pd_grande

all: $(BINS)

$(ALG)/mochila_pd: $(ALG)/mochila_pd.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

$(ALG)/mochila_bt: $(ALG)/mochila_bt.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

$(ALG)/mochila_bb: $(ALG)/mochila_bb.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

$(ALG)/mochila_pd_grande: $(ALG)/mochila_pd_grande.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

teste: all
	$(PY) experimentos/teste_random.py $(ARGS)

experimentos: all
	$(PY) experimentos/rodar_experimentos.py $(ARGS)

estatistica:
	$(PY) experimentos/analise_estatistica.py

graficos:
	$(PY) experimentos/gerar_graficos.py

relatorio:
	node relatorio/build_relatorio.js

limpar:
	rm -f $(BINS)
	rm -rf resultados instancias

.PHONY: all teste experimentos estatistica graficos relatorio limpar
