# Mini Motor de Busca Semântico para Notícias Econômicas

## Objetivo

Este projeto foi desenvolvido como solução para o desafio técnico de estágio em Ciência de Dados do FGV IBRE.

O objetivo consiste em construir um mini motor de busca semântico capaz de recuperar notícias econômicas relevantes a partir de consultas em linguagem natural.

O pipeline foi dividido em três etapas principais:

- Limpeza e tratamento textual
- Geração de embeddings semânticos
- Busca por similaridade semântica

---

# Estrutura do Projeto

```bash
├── dados/
│   └── noticias_brutas.json
│
├── dados_limpos/
│   └── noticias_limpas.json
│
├── embeddings.npy
│
├── limpeza.py
├── embeddings.py
├── busca_semantica.py
│
└── README.md
```

---

# Tecnologias Utilizadas

- Python
- Pandas
- BeautifulSoup
- Regex (re)
- Sentence Transformers
- NumPy

---

# Etapa 1 — Limpeza e Tratamento de Texto

Nesta etapa foi realizado o pré-processamento dos textos das notícias.

Os principais tratamentos aplicados foram:

- Remoção de tags HTML
- Conversão de entidades HTML
- Remoção de timestamps e metadados
- Normalização de espaços em branco
- Identificação de textos inválidos ou muito curtos

Também foi criada uma coluna chamada `validacao`, classificando os artigos entre:

- Válido
- Inválido

Critério utilizado:

- textos com mais de 50 caracteres foram considerados válidos.

O resultado final foi salvo em:

```bash
dados_limpos/noticias_limpas.json
```

---

# Etapa 2 — Geração de Embeddings

Para representar semanticamente os textos, foi utilizado o modelo:

`paraphrase-multilingual-MiniLM-L12-v2`

da biblioteca Sentence Transformers.

## Justificativa da escolha

O modelo foi escolhido por:

- possuir suporte multilíngue;
- funcionar bem para similaridade semântica;
- apresentar baixo custo computacional;
- ser adequado para textos em português.

Cada notícia válida foi convertida em um vetor numérico (embedding), permitindo comparar semanticamente os conteúdos.

Os embeddings foram salvos localmente no arquivo:

```bash
embeddings.npy
```

---

# Etapa 3 — Busca Semântica

A busca semântica recebe uma consulta em linguagem natural e retorna os artigos mais relevantes com base na similaridade de cosseno entre embeddings.

## Funcionamento

1. A consulta é convertida em embedding;
2. A similaridade entre consulta e artigos é calculada;
3. Os artigos mais similares são retornados.

Foi utilizada a função:

```python
util.cos_sim()
```

da biblioteca Sentence Transformers.

---

# Consultas Utilizadas

As seguintes queries foram utilizadas para validação:

```python
buscar("mudanças na taxa de juros")
buscar("mercado de trabalho e desemprego")
buscar("inflação e preços ao consumidor")
```
