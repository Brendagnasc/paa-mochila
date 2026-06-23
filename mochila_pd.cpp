// mochila_pd.cpp
// Mochila 0-1 com duas restricoes (peso W e volume V) - PROGRAMACAO DINAMICA
//
// Estrategia: tabela dp[i][a][b] = maior valor usando os primeiros i itens,
// com capacidade de peso a e capacidade de volume b.
//   dp[i][a][b] = max( dp[i-1][a][b],                              (nao leva o item i)
//                      dp[i-1][a-w_i][b-l_i] + v_i )               (leva o item i, se couber)
//
// Complexidade de tempo:  O(n * W * V)
// Complexidade de espaco: O(n * W * V)  (tabela completa para reconstruir os itens)
//
// Entrada (argv[1] ou stdin):
//   1a linha:  W  V
//   demais:    peso  volume  valor   (separados por espaco/tabulacao)
//
// Saida: lucro maximo, itens na mochila (indices 1..n) e tempo de execucao.

#include <bits/stdc++.h>
using namespace std;

int main(int argc, char** argv) {
    istream* in = &cin;
    ifstream fin;
    if (argc >= 2) {
        fin.open(argv[1]);
        if (!fin) { cerr << "Erro ao abrir arquivo: " << argv[1] << "\n"; return 1; }
        in = &fin;
    }

    int W, V;
    if (!(*in >> W >> V)) { cerr << "Entrada invalida\n"; return 1; }

    vector<int> w, l, val;
    int pw, pl, pv;
    while (*in >> pw >> pl >> pv) { w.push_back(pw); l.push_back(pl); val.push_back(pv); }
    int n = (int)w.size();

    auto t0 = chrono::high_resolution_clock::now();

    const size_t A = (size_t)W + 1, B = (size_t)V + 1;
    vector<int> dp((size_t)(n + 1) * A * B, 0);
    auto idx = [&](int i, int a, int b) -> size_t { return ((size_t)i * A + a) * B + b; };

    for (int i = 1; i <= n; i++) {
        int wi = w[i - 1], li = l[i - 1], vi = val[i - 1];
        for (int a = 0; a <= W; a++) {
            for (int b = 0; b <= V; b++) {
                int best = dp[idx(i - 1, a, b)];
                if (wi <= a && li <= b) {
                    int cand = dp[idx(i - 1, a - wi, b - li)] + vi;
                    if (cand > best) best = cand;
                }
                dp[idx(i, a, b)] = best;
            }
        }
    }

    long long lucro = dp[idx(n, W, V)];

    // Reconstrucao: compara dp[i] com dp[i-1] para saber se o item i foi usado.
    vector<int> chosen;
    int a = W, b = V;
    for (int i = n; i >= 1; i--) {
        if (dp[idx(i, a, b)] != dp[idx(i - 1, a, b)]) {
            chosen.push_back(i);            // indice 1..n na ordem de entrada
            a -= w[i - 1];
            b -= l[i - 1];
        }
    }
    sort(chosen.begin(), chosen.end());

    auto t1 = chrono::high_resolution_clock::now();
    double secs = chrono::duration<double>(t1 - t0).count();

    cout << "Lucro maximo: " << lucro << "\n";
    cout << "Itens na mochila:";
    for (int c : chosen) cout << " " << c;
    cout << "\n";
    cout << fixed << setprecision(6);
    cout << "Tempo de execucao: " << secs << " s\n";
    return 0;
}
