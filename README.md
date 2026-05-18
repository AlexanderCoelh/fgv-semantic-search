# Mini Motor de Busca Semântico — Notícias Econômicas

Este projeto foi desenvolvido como solução para o desafio técnico de estágio em
Ciência de Dados do FGV IBRE. O objetivo é construir um mini motor de busca
semântico capaz de recuperar notícias econômicas relevantes a partir de consultas
em linguagem natural — sem depender de palavras-chave exatas.

---

## Estrutura do Projeto

```text
├── dados/
│   └── noticias_brutas.json
├── dados_limpos/
│   └── noticias_limpas.json
├── embeddings.npy
├── etapa1_limpeza.py
├── etapa2_embeddings.py
├── etapa3_busca.py
└── README.md
```

---

## Como rodar o projeto

1. Clone o repositório e instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute as etapas em ordem:

```bash
python etapa1_limpeza.py
python etapa2_embeddings.py
python etapa3_busca.py
```

Na primeira execução, o modelo será baixado automaticamente (~400MB).

---

## Etapa 1 — Limpeza e Tratamento de Texto

Os textos brutos continham vários tipos de sujeira que precisavam ser tratados
antes de qualquer análise. Os principais problemas encontrados foram tags e
entidades HTML, timestamps embutidos no corpo do texto e espaços em excesso.

Para remover as tags e decodificar as entidades HTML, usei a biblioteca
BeautifulSoup — que lida com HTML de forma mais robusta do que regex puro.
A parte mais trabalhosa foi remover os timestamps, já que apareciam em formatos
variados (como "Publicado em: 02/08/2023 às 20h15" ou "23/08/2023 - 18h45 |
Mercados"), o que exigiu alguns padrões de regex diferentes para cobrir todos
os casos.

Também identifiquei um artigo com conteúdo mínimo (id 18, texto: "Selic.").
Para tratar esse caso, criei uma coluna chamada `validacao` que classifica cada
artigo como "Válido" ou "Inválido" com base no tamanho do texto limpo — textos
com mais de 50 caracteres foram considerados válidos. Esse critério foi suficiente
para isolar o caso extremo sem descartar nenhum artigo legítimo.

O resultado foi salvo em `dados_limpos/noticias_limpas.json`.

---

## Etapa 2 — Geração de Embeddings

Para transformar os textos em vetores numéricos, usei a biblioteca
`sentence-transformers` com o modelo `paraphrase-multilingual-MiniLM-L12-v2`.

Esse modelo foi escolhido por três motivos principais: funciona bem em português,
foi treinado especificamente para comparar similaridade semântica entre frases, e
é leve o suficiente para rodar sem GPU. Para um corpus pequeno como esse, ele é
mais do que suficiente.

Cada artigo válido foi convertido em um vetor de 384 dimensões. Os embeddings
foram salvos em `embeddings.npy` para reutilização na etapa seguinte.

---

## Etapa 3 — Busca Semântica

A busca recebe uma consulta em texto livre, gera o embedding da query com o mesmo
modelo e calcula a similaridade de cosseno entre a query e todos os artigos.
Os 3 artigos com maior score são retornados.

---

## Avaliação dos Resultados

Os resultados das três queries obrigatórias foram satisfatórios e demonstram que
o motor consegue recuperar artigos relevantes mesmo sem correspondência exata
de palavras.

### "mudanças na taxa de juros"

Retornou artigos sobre a manutenção da Selic, projeções de corte de juros e
crédito — todos diretamente relacionados à política monetária. O modelo conseguiu
associar "taxa de juros" a "Selic" sem que a palavra aparecesse na query.

### "mercado de trabalho e desemprego"

Os dois primeiros resultados foram muito precisos: um sobre desemprego juvenil e
outro sobre a queda da taxa de desemprego para 7,9%. O terceiro, sobre o setor
de serviços, também faz sentido — o setor é o maior empregador do Brasil e o
artigo menciona explicitamente a melhora no mercado de trabalho.

### "inflação e preços ao consumidor"

O primeiro resultado foi sobre o IPA (inflação ao produtor), que tem relação
direta com os preços ao consumidor. O segundo trouxe um artigo sobre a Selic,
o que também é relevante já que a taxa de juros é o principal instrumento de
controle da inflação no Brasil.

De forma geral, o motor apresentou bom desempenho para um corpus de apenas 19
artigos, com scores entre 0.45 e 0.64 — indicando similaridade semântica
consistente.
