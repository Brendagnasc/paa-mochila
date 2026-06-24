// mochila_pd_grande.cpp
// Mochila 0-1 com duas restricoes - PROGRAMACAO DINAMICA (memoria otimizada)
//
// Versao para instancias GRANDES. Mantem o mesmo tempo O(n . W . V) da versao
// padrao, mas reduz o espaco dos valores de O(n . W . V) para O(W . V), usando
// apenas duas camadas (anterior e atual) em vez da tabela 3D inteira.
//
// Para ainda reconstruir os itens, guardamos so 1 BIT por (item, a, b) indicando
// se o item foi levado, em vez de um inteiro de 32 bits. Isso reduz a memoria de
// reconstrucao em 32x (ex.: n=1000, W=V=300 passa de ~363 MB para ~11 MB).
//
// Entrada/Saida: identicas as outras implementacoes.

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

    const size_t B = (size_t)V + 1;
    const size_t cells = (size_t)(W + 1) * B;          // celulas de uma camada
    auto pos = [&](int a, int b) -> size_t { return (size_t)a * B + b; };

    vector<int> prev(cells, 0), cur(cells, 0);

    // 1 bit por (item, a, b): item i foi levado para chegar ao otimo em (a,b)?
    const size_t total_bits = (size_t)n * cells;
    vector<uint8_t> take((total_bits + 7) / 8, 0);
    auto set_bit = [&](size_t g) { take[g >> 3] |= (uint8_t)(1u << (g & 7)); };
    auto get_bit = [&](size_t g) -> bool { return (take[g >> 3] >> (g & 7)) & 1u; };

    for (int i = 0; i < n; i++) {
        int wi = w[i], li = l[i], vi = val[i];
        size_t base = (size_t)i * cells;
        for (int a = 0; a <= W; a++) {
            for (int b = 0; b <= V; b++) {
                size_t idx = pos(a, b);
                int best = prev[idx];
                if (wi <= a && li <= b) {
                    int cand = prev[pos(a - wi, b - li)] + vi;
                    if (cand > best) { best = cand; set_bit(base + idx); }
                }
                cur[idx] = best;
            }
        }
        swap(prev, cur);   // 'prev' passa a ser a camada do item i
    }

    long long lucro = prev[pos(W, V)];

    // Reconstrucao usando os bits de decisao.
    vector<int> chosen;
    int a = W, b = V;
    for (int i = n - 1; i >= 0; i--) {
        size_t g = (size_t)i * cells + pos(a, b);
        if (get_bit(g)) {
            chosen.push_back(i + 1);   // indice 1..n
            a -= w[i];
            b -= l[i];
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
