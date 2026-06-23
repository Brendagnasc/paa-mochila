// mochila_bt.cpp
// Mochila 0-1 com duas restricoes (peso W e volume V) - BACKTRACKING
//
// Estrategia: arvore de decisao (leva / nao leva) para cada item.
// Poda apenas por VIABILIDADE: so descemos pelo ramo "leva o item" se ele
// ainda couber no peso E no volume restantes. Nao ha funcao de limite
// (essa e a diferenca para o branch-and-bound).
//
// Complexidade de tempo:  O(2^n) no pior caso.
// Complexidade de espaco: O(n)  (profundidade da recursao + melhor selecao).
//
// Entrada/Saida: mesmo formato das outras implementacoes.

#include <bits/stdc++.h>
using namespace std;

int n, W, V;
vector<int> w, l, val;
long long best;
vector<int> bestSel;   // melhor conjunto encontrado (indices 1..n)
vector<int> cur;       // selecao atual

void bt(int k, int cw, int cv, long long cval) {
    if (cval > best) { best = cval; bestSel = cur; }
    if (k == n) return;

    // Ramo 1: levar o item k (apenas se couber nas duas restricoes)
    if (cw + w[k] <= W && cv + l[k] <= V) {
        cur.push_back(k + 1);
        bt(k + 1, cw + w[k], cv + l[k], cval + val[k]);
        cur.pop_back();
    }
    // Ramo 2: nao levar o item k
    bt(k + 1, cw, cv, cval);
}

int main(int argc, char** argv) {
    istream* in = &cin;
    ifstream fin;
    if (argc >= 2) {
        fin.open(argv[1]);
        if (!fin) { cerr << "Erro ao abrir arquivo: " << argv[1] << "\n"; return 1; }
        in = &fin;
    }

    if (!(*in >> W >> V)) { cerr << "Entrada invalida\n"; return 1; }
    int pw, pl, pv;
    while (*in >> pw >> pl >> pv) { w.push_back(pw); l.push_back(pl); val.push_back(pv); }
    n = (int)w.size();

    auto t0 = chrono::high_resolution_clock::now();

    best = 0;
    bt(0, 0, 0, 0);

    auto t1 = chrono::high_resolution_clock::now();
    double secs = chrono::duration<double>(t1 - t0).count();

    sort(bestSel.begin(), bestSel.end());
    cout << "Lucro maximo: " << best << "\n";
    cout << "Itens na mochila:";
    for (int c : bestSel) cout << " " << c;
    cout << "\n";
    cout << fixed << setprecision(6);
    cout << "Tempo de execucao: " << secs << " s\n";
    return 0;
}
