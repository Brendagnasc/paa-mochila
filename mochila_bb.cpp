// mochila_bb.cpp
// Mochila 0-1 com duas restricoes (peso W e volume V) - BRANCH-AND-BOUND
//
// Estrategia: mesma arvore de decisao do backtracking, mas com uma FUNCAO DE
// LIMITE (bound) que estima o melhor valor ainda alcancavel a partir do no
// atual. Se esse limite nao for capaz de superar a melhor solucao ja achada,
// o ramo inteiro e podado.
//
// Limite (relaxacao fracionaria pelo PESO):
//   Ignoramos temporariamente a restricao de volume e resolvemos a mochila
//   fracionaria sobre o peso restante, processando os itens em ordem
//   decrescente de densidade valor/peso. Como remover uma restricao e permitir
//   fracoes so pode AUMENTAR o otimo, o resultado e um limite superior valido
//   para o problema com as duas restricoes.
//
// Complexidade de tempo:  O(2^n) no pior caso (mas com podas costuma ser
//                         muito mais rapido que o backtracking puro).
//                         Ordenacao inicial: O(n log n).
// Complexidade de espaco: O(n).
//
// Entrada/Saida: mesmo formato das outras implementacoes.

#include <bits/stdc++.h>
using namespace std;

struct Item { int w, l, val, orig; };  // orig = indice 1..n na ordem de entrada

int n, W, V;
vector<Item> it;          // itens ordenados por densidade valor/peso (desc)
long long best;
vector<int> bestSel, cur;

// Limite superior a partir do item k, com peso ja usado cw e valor ja obtido cval.
double bound(int k, int cw, long long cval) {
    double ub = (double)cval;
    int remW = W - cw;
    for (int j = k; j < n && remW > 0; j++) {
        if (it[j].w <= remW) { remW -= it[j].w; ub += it[j].val; }
        else { ub += (double)it[j].val * ((double)remW / it[j].w); break; }
    }
    return ub;
}

void bb(int k, int cw, int cv, long long cval) {
    if (cval > best) { best = cval; bestSel = cur; }
    if (k == n) return;

    // Poda por limite: se nem o melhor caso possivel supera 'best', abandona.
    if (bound(k, cw, cval) <= (double)best + 1e-9) return;

    // Ramo 1: levar o item k (apenas se couber nas duas restricoes)
    if (cw + it[k].w <= W && cv + it[k].l <= V) {
        cur.push_back(it[k].orig);
        bb(k + 1, cw + it[k].w, cv + it[k].l, cval + it[k].val);
        cur.pop_back();
    }
    // Ramo 2: nao levar o item k
    bb(k + 1, cw, cv, cval);
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
    int pw, pl, pv, id = 0;
    while (*in >> pw >> pl >> pv) { it.push_back({pw, pl, pv, ++id}); }
    n = (int)it.size();

    auto t0 = chrono::high_resolution_clock::now();

    // Ordena por densidade valor/peso decrescente (comparacao cruzada, sem float).
    sort(it.begin(), it.end(), [](const Item& a, const Item& b) {
        return (long long)a.val * b.w > (long long)b.val * a.w;
    });

    best = 0;
    bb(0, 0, 0, 0);

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
