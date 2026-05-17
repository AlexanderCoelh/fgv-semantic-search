import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

#Carrega as noticias limpas e válidas, além do embeddings e o modelo de linguagem
df = pd.read_json("dados_limpos/noticias_limpas.json")
df_valido = df[df['validacao'] == "Válido"].reset_index(drop=True)
embeddings = np.load('embeddings.npy')
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Função para receber uma consulta e retornar os artigos mais relevantes
def buscar(texto, top_k=3):
    vetor_consulta = modelo.encode(texto)
    similaridade = util.cos_sim(vetor_consulta, embeddings)[0]
    melhores = similaridade.argsort(descending=True)[:top_k]

    for posicao in melhores:
        artigo = df_valido.iloc[int(posicao)] 
        print("score:", round(float(similaridade[posicao]), 4))
        print(artigo["titulo"])
        print()

buscar("mudanças na taxa de juros")
buscar("mercado de trabalho e desemprego")
buscar("inflação e preços ao consumidor")