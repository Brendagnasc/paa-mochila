const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageNumber, PageBreak,
} = require("docx");

const RAIZ = path.join(__dirname, "..");
const CONTENT_W = 9026; // A4, margens de 1 polegada
const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border };

// ---------- helpers ----------
function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { after: opts.after ?? 120, line: 276 },
    children: [new TextRun({ text, bold: opts.bold, italics: opts.italics })],
  });
}
function runs(children, opts = {}) {
  return new Paragraph({
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { after: opts.after ?? 120, line: 276 },
    children,
  });
}
function h1(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(text)] });
}
function h2(text) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(text)] });
}
function it(t) { return new TextRun({ text: t, italics: true }); }
function tx(t) { return new TextRun({ text: t }); }

function cell(text, { headerRow = false, w, bold = false, align = AlignmentType.LEFT } = {}) {
  return new TableCell({
    borders,
    width: { size: w, type: WidthType.DXA },
    shading: headerRow ? { fill: "D9E2F3", type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 110, right: 110 },
    children: [new Paragraph({
      alignment: align,
      spacing: { after: 0, line: 252 },
      children: [new TextRun({ text, bold: bold || headerRow })],
    })],
  });
}

function img(path, caption) {
  const data = fs.readFileSync(path);
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60 },
      children: [new ImageRun({
        type: "png", data,
        transformation: { width: 460, height: 288 },
        altText: { title: caption, description: caption, name: caption },
      })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 160 },
      children: [new TextRun({ text: caption, italics: true, size: 20 })],
    }),
  ];
}

// ---------- tabela de complexidade ----------
const wA = [2600, 3213, 3213];
const tabComplexidade = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: wA,
  rows: [
    new TableRow({ tableHeader: true, children: [
      cell("Algoritmo", { headerRow: true, w: wA[0] }),
      cell("Tempo (pior caso)", { headerRow: true, w: wA[1] }),
      cell("Espaco", { headerRow: true, w: wA[2] }),
    ]}),
    new TableRow({ children: [
      cell("Programacao dinamica", { w: wA[0] }),
      cell("O(n . W . V)", { w: wA[1] }),
      cell("O(n . W . V)", { w: wA[2] }),
    ]}),
    new TableRow({ children: [
      cell("Backtracking", { w: wA[0] }),
      cell("O(2^n)", { w: wA[1] }),
      cell("O(n)", { w: wA[2] }),
    ]}),
    new TableRow({ children: [
      cell("Branch-and-bound", { w: wA[0] }),
      cell("O(2^n)", { w: wA[1] }),
      cell("O(n)", { w: wA[2] }),
    ]}),
  ],
});

// ---------- tabela de resultados ----------
const wR = [1300, 1300, 1300, 1709, 1709, 1708];
function rowRes(n, W, V, pd, bt, bb) {
  return new TableRow({ children: [
    cell(n, { w: wR[0], align: AlignmentType.CENTER }),
    cell(W, { w: wR[1], align: AlignmentType.CENTER }),
    cell(V, { w: wR[2], align: AlignmentType.CENTER }),
    cell(pd, { w: wR[3], align: AlignmentType.CENTER }),
    cell(bt, { w: wR[4], align: AlignmentType.CENTER }),
    cell(bb, { w: wR[5], align: AlignmentType.CENTER }),
  ]});
}
const tabResultados = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: wR,
  rows: [
    new TableRow({ tableHeader: true, children: [
      cell("n", { headerRow: true, w: wR[0], align: AlignmentType.CENTER }),
      cell("W", { headerRow: true, w: wR[1], align: AlignmentType.CENTER }),
      cell("V", { headerRow: true, w: wR[2], align: AlignmentType.CENTER }),
      cell("PD (s)", { headerRow: true, w: wR[3], align: AlignmentType.CENTER }),
      cell("BT (s)", { headerRow: true, w: wR[4], align: AlignmentType.CENTER }),
      cell("BB (s)", { headerRow: true, w: wR[5], align: AlignmentType.CENTER }),
    ]}),
    rowRes("10", "30", "30", "0,000031", "0,000008", "0,000003"),
    rowRes("15", "45", "45", "0,000082", "0,000111", "0,000005"),
    rowRes("20", "60", "60", "0,000183", "0,003375", "0,000009"),
    rowRes("20", "25", "25", "0,000043", "0,000103", "0,000008"),
    rowRes("20", "50", "50", "0,000125", "0,002084", "0,000017"),
    rowRes("20", "75", "75", "0,000440", "0,004462", "0,000015"),
    rowRes("20", "100", "100", "0,000506", "0,005210", "0,000005"),
    rowRes("20", "125", "125", "0,000711", "0,005312", "0,000004"),
  ],
});

// ---------- documento ----------
const children = [];

// Titulo e autores
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 80 },
  children: [new TextRun({
    text: "Avaliacao empirica de algoritmos para o problema da mochila 0-1 com duas restricoes",
    bold: true, size: 32,
  })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: "Brenda Gabrielle Alves Nascimento, [Aluno 2], [Aluno 3], [Aluno 4]", size: 24 })],
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: [new TextRun({
    text: "Departamento de Computacao, Universidade Federal de Ouro Preto (UFOP) - Projeto e Analise de Algoritmos (BCC241)",
    italics: true, size: 20,
  })],
}));

// Resumo
children.push(h2("Resumo"));
children.push(runs([
  it("Este trabalho apresenta a avaliacao empirica de tres algoritmos exatos para o problema da mochila 0-1 com duas restricoes simultaneas, peso e volume: programacao dinamica, backtracking e branch-and-bound. As tres implementacoes foram desenvolvidas em C++ e comparadas sobre instancias geradas aleatoriamente, variando-se a quantidade de itens e as capacidades da mochila. Para cada combinacao de parametros foram executadas dez instancias, e a hipotese de empate estatistico entre os algoritmos foi avaliada pelo teste de Friedman, com pos-teste de Wilcoxon corrigido por Bonferroni. Os resultados confirmam o comportamento teorico esperado: o backtracking cresce exponencialmente com o numero de itens, enquanto a programacao dinamica cresce de forma polinomial e o branch-and-bound, gracas a poda por limite, foi o mais rapido em praticamente todas as combinacoes."),
]));

// 1. Introducao
children.push(h1("1. Introducao"));
children.push(p("O problema da mochila 0-1 e um problema classico de otimizacao combinatoria. Na variante estudada neste trabalho, a mochila possui duas restricoes simultaneas: ela suporta no maximo W quilos e V litros. Dispoe-se de n itens, e cada item i possui peso w_i, volume l_i e valor v_i. Cada item pode ser levado inteiro ou nao ser levado (nao ha repeticao nem fracionamento). O objetivo e selecionar um subconjunto de itens que maximize o valor total transportado, respeitando ao mesmo tempo o limite de peso e o limite de volume."));
children.push(p("A presenca de uma segunda restricao distingue o problema da mochila classica de uma unica restricao, tanto na modelagem quanto no custo computacional. O objetivo deste trabalho e implementar tres estrategias exatas para o problema e compara-las empiricamente quanto ao tempo de execucao, observando como cada uma se comporta a medida que o tamanho da entrada cresce."));
children.push(p("De forma resumida, os experimentos mostraram que o branch-and-bound foi o algoritmo mais rapido na maioria dos cenarios, que o backtracking se torna rapidamente inviavel conforme o numero de itens e a folga das capacidades aumentam, e que a programacao dinamica apresenta um custo previsivel que cresce proporcionalmente ao produto n . W . V."));
children.push(p("O restante do documento esta organizado da seguinte forma. A Secao 2 descreve os tres algoritmos e suas analises de complexidade de tempo e espaco. A Secao 3 apresenta a avaliacao experimental, incluindo a configuracao dos experimentos, a metrica de avaliacao, a metodologia estatistica e os resultados obtidos. A Secao 4 traz as conclusoes, e a Secao 5 lista as referencias."));

// 2. Algoritmos
children.push(h1("2. Descricao dos algoritmos e analise de complexidade"));

children.push(h2("2.1. Programacao dinamica"));
children.push(p("A abordagem de programacao dinamica resolve o problema preenchendo uma tabela tridimensional dp[i][a][b], que armazena o maior valor possivel usando apenas os primeiros i itens, com capacidade de peso a e capacidade de volume b. A relacao de recorrencia considera, para cada item, a decisao de leva-lo ou nao:"));
children.push(runs([it("dp[i][a][b] = max( dp[i-1][a][b],  dp[i-1][a - w_i][b - l_i] + v_i )")], { align: AlignmentType.CENTER }));
children.push(p("em que o segundo termo so e considerado quando o item cabe no peso e no volume restantes (w_i <= a e l_i <= b). A resposta otima esta em dp[n][W][V], e os itens escolhidos sao recuperados percorrendo a tabela de tras para frente, comparando dp[i][a][b] com dp[i-1][a][b] para decidir se o item i foi utilizado."));
children.push(p("Como a tabela possui (n+1)(W+1)(V+1) posicoes e cada posicao e calculada em tempo constante, o custo de tempo e O(n . W . V). O custo de espaco e o mesmo, O(n . W . V), pois a tabela completa e mantida para permitir a reconstrucao da solucao. Vale notar que o consumo de memoria pode ser reduzido para O(W . V) usando apenas duas camadas da tabela, ao custo de armazenar separadamente as decisoes para reconstruir os itens."));

children.push(h2("2.2. Backtracking"));
children.push(p("O backtracking percorre a arvore de decisao do problema: para cada item, ha dois ramos, levar ou nao levar. A unica poda aplicada e por viabilidade, ou seja, o ramo que leva um item so e explorado quando o item ainda cabe no peso e no volume disponiveis. Nao ha nenhuma estimativa sobre a qualidade da solucao que cada ramo pode alcancar, o que diferencia esta estrategia do branch-and-bound."));
children.push(p("No pior caso, a arvore possui um numero de nos proporcional a 2^n, de modo que o tempo de execucao e O(2^n). O espaco e O(n), correspondente a profundidade da recursao e ao armazenamento da melhor selecao corrente. Na pratica, a poda por viabilidade reduz a arvore de forma significativa quando as capacidades sao pequenas em relacao ao tamanho dos itens, pois poucos itens cabem simultaneamente."));

children.push(h2("2.3. Branch-and-bound"));
children.push(p("O branch-and-bound utiliza a mesma arvore de decisao do backtracking, porem acrescenta uma funcao de limite (bound) que estima, de forma otimista, o melhor valor ainda alcancavel a partir de cada no. Se esse limite nao for capaz de superar a melhor solucao ja encontrada, o ramo inteiro e descartado, evitando exploracao desnecessaria."));
children.push(p("O limite e calculado por uma relaxacao fracionaria sobre a restricao de peso: ignora-se temporariamente o volume e resolve-se a mochila fracionaria, processando os itens em ordem decrescente de densidade valor/peso e preenchendo a capacidade de peso restante, inclusive de forma fracionada no ultimo item. Como remover a restricao de volume e permitir fracoes apenas pode aumentar o valor otimo, o resultado e um limite superior valido para o problema original com as duas restricoes."));
children.push(p("No pior caso o branch-and-bound ainda e O(2^n), pois a poda pode nao ocorrer; a ordenacao inicial por densidade custa O(n log n) e o espaco e O(n). Entretanto, como mostram os experimentos, a poda por limite costuma reduzir drasticamente o tempo de execucao, tornando esta a estrategia mais eficiente na maioria das instancias avaliadas."));

children.push(h2("2.4. Resumo das complexidades"));
children.push(tabComplexidade);
children.push(new Paragraph({ spacing: { after: 160 }, children: [] }));

// 3. Avaliacao experimental
children.push(new Paragraph({ pageBreakBefore: true, heading: HeadingLevel.HEADING_1, children: [new TextRun("3. Avaliacao experimental")] }));

children.push(h2("3.1. Configuracao dos experimentos"));
children.push(p("As instancias foram geradas aleatoriamente. Os atributos de cada item, peso e volume, foram sorteados uniformemente no intervalo de 1 a 10, e o valor no intervalo de 1 a 100, mantendo essas faixas fixas em todos os experimentos. As capacidades W e V da mochila foram os parametros variados. Para garantir reprodutibilidade, a geracao usa sementes deterministicas, de modo que as mesmas instancias sao obtidas a cada execucao. Para cada combinacao de parametros foram geradas e avaliadas dez instancias independentes."));
children.push(p("Os experimentos foram organizados em duas varreduras. Na primeira, estuda-se o efeito da quantidade de itens: o numero de itens n varia, e as capacidades acompanham esse crescimento (W = V = 3n), de forma a manter o regime em que aproximadamente metade dos itens cabe na mochila, que e o regime mais dificil para os algoritmos exponenciais. Na segunda varredura, estuda-se o efeito da capacidade: fixa-se n = 20 e variam-se as capacidades W = V nos valores 25, 50, 75, 100 e 125, isolando o efeito do produto W . V sobre a programacao dinamica."));
children.push(runs([
  tx("As medicoes deste relatorio foram obtidas em "),
  it("[descrever o equipamento: processador, memoria, sistema operacional e compilador, por exemplo g++ 11 com otimizacao -O2]"),
  tx(". Foi imposto um limite de tempo por execucao; quando um algoritmo o ultrapassa, a execucao e registrada como tempo esgotado, o que ja constitui um resultado relevante sobre a inviabilidade do metodo naquele tamanho."),
]));

children.push(h2("3.2. Metrica de avaliacao"));
children.push(p("A metrica de avaliacao e o tempo de execucao, medido internamente em cada programa apenas em torno do nucleo do algoritmo, sem incluir a leitura do arquivo de entrada. Para cada combinacao de parametros relata-se a media dos tempos das dez instancias."));

children.push(h2("3.3. Metodologia estatistica"));
children.push(p("Para verificar se houve empate estatistico entre os algoritmos em cada combinacao de parametros, aplicou-se um teste estatistico por combinacao. Como as dez instancias foram resolvidas pelos tres algoritmos, as medidas sao pareadas, e o teste adequado e o de Friedman, um teste nao parametrico para amostras relacionadas. A hipotese nula e a de que nao ha diferenca entre os tempos dos tres algoritmos; quando o valor-p e inferior ao nivel de significancia adotado (alpha = 0,05), rejeita-se essa hipotese e conclui-se que ha diferenca significativa. Nos casos em que o teste de Friedman acusa diferenca, aplica-se um pos-teste de Wilcoxon dos postos sinalizados, par a par, com correcao de Bonferroni, para identificar quais pares de algoritmos diferem e quais empatam."));

children.push(h2("3.4. Resultados"));
children.push(p("A Tabela 2 apresenta o tempo medio de execucao de cada algoritmo, em segundos, para as combinacoes avaliadas. A Figura 1 mostra o crescimento do tempo em funcao da quantidade de itens, e a Figura 2 o crescimento em funcao da capacidade da mochila; em ambas o eixo vertical esta em escala logaritmica, o que torna visiveis simultaneamente o comportamento exponencial e o polinomial."));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 60, after: 60 },
  children: [new TextRun({ text: "Tabela 2. Tempo medio de execucao por combinacao (segundos).", italics: true, size: 20 })],
}));
children.push(tabResultados);
children.push(runs([
  it("Observacao: os valores acima sao ilustrativos, obtidos em uma rodada de demonstracao. Substitua-os pelos numeros da rodada final do grupo, executada no equipamento descrito na Secao 3.1. Em todas as combinacoes o teste de Friedman indicou diferenca significativa (valor-p < 0,05) entre os tres algoritmos."),
], { after: 160 }));
img(path.join(RAIZ, "resultados", "tempo_vs_n.png"), "Figura 1. Tempo de execucao em funcao da quantidade de itens (W = V = 3n), escala logaritmica.").forEach(x => children.push(x));
img(path.join(RAIZ, "resultados", "tempo_vs_capacidade.png"), "Figura 2. Tempo de execucao em funcao da capacidade (n = 20, W = V), escala logaritmica.").forEach(x => children.push(x));

children.push(h2("3.5. Comentarios"));
children.push(p("Os resultados confirmam o comportamento previsto pela analise de complexidade. Na Figura 1, em escala logaritmica, o backtracking aparece como uma reta de inclinacao acentuada, caracteristica de crescimento exponencial, ao passo que a programacao dinamica e o branch-and-bound permanecem quase planos, refletindo um crescimento muito mais lento. Existe um ponto de cruzamento a partir do qual o backtracking, inicialmente competitivo para poucos itens, passa a ser o mais lento dos tres."));
children.push(p("A Figura 2 evidencia o efeito da capacidade. O tempo da programacao dinamica cresce de maneira constante com o aumento de W e V, coerente com o custo O(n . W . V), ja que com n fixo o tempo passa a depender do produto W . V. O backtracking cresce rapidamente e tende a estabilizar quando a capacidade e grande o suficiente para que quase todos os itens caibam. O branch-and-bound mantem-se sempre na faixa mais baixa e chega a melhorar para capacidades muito grandes, pois nesse regime a solucao tende a incluir quase todos os itens e o limite poda a busca muito cedo."));
children.push(p("Quanto a corretude, as tres implementacoes produziram exatamente o mesmo valor otimo em todas as instancias avaliadas, o que serve como validacao cruzada dos algoritmos. As diferencas de desempenho, confirmadas estatisticamente pelo teste de Friedman, mostram que a escolha do algoritmo tem impacto pratico relevante mesmo para instancias de tamanho moderado."));

// 4. Conclusao
children.push(h1("4. Conclusao"));
children.push(p("Este trabalho implementou e comparou empiricamente tres algoritmos exatos para o problema da mochila 0-1 com duas restricoes. A programacao dinamica oferece um tempo previsivel, polinomial no numero de itens, mas com consumo de tempo e memoria proporcional ao produto das capacidades, o que a torna sensivel a instancias com capacidades muito grandes. O backtracking e simples, porem seu custo exponencial o torna inviavel rapidamente conforme cresce o numero de itens, sobretudo quando muitos itens cabem na mochila. O branch-and-bound, ao incorporar uma funcao de limite, foi o algoritmo mais eficiente na grande maioria das combinacoes avaliadas, combinando a generalidade da busca exaustiva com uma poda eficaz. Como trabalho futuro, o limite do branch-and-bound poderia ser refinado para considerar tambem a restricao de volume, o que tende a fortalecer a poda em instancias limitadas pelo volume."));

// 5. Referencias
children.push(h1("5. Referencias"));
const refs = [
  "CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. Algoritmos: teoria e pratica. 3. ed. Rio de Janeiro: Elsevier, 2012.",
  "KELLERER, H.; PFERSCHY, U.; PISINGER, D. Knapsack Problems. Berlin: Springer, 2004.",
  "HOROWITZ, E.; SAHNI, S. Fundamentals of Computer Algorithms. Rockville: Computer Science Press, 1978.",
  "FRIEDMAN, M. The use of ranks to avoid the assumption of normality implicit in the analysis of variance. Journal of the American Statistical Association, v. 32, n. 200, p. 675-701, 1937.",
  "DEMSAR, J. Statistical comparisons of classifiers over multiple data sets. Journal of Machine Learning Research, v. 7, p. 1-30, 2006.",
];
refs.forEach(r => children.push(new Paragraph({
  alignment: AlignmentType.JUSTIFIED,
  spacing: { after: 100, line: 276 },
  indent: { left: 360, hanging: 360 },
  children: [new TextRun({ text: r })],
})));

// ---------- montagem ----------
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 140 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 160, after: 100 }, outlineLevel: 1 } },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "", size: 20 }),
          new TextRun({ children: [PageNumber.CURRENT], size: 20 })],
      })] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(path.join(RAIZ, "relatorio_mochila.docx"), buffer);
  console.log("relatorio_mochila.docx gerado");
});
