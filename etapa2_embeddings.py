import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Carregando os dados e filtrando as válidas
noticias = pd.read_json("dados_limpos/noticias_limpas.json")
noticias_validas = noticias[noticias['validacao'] == "Válido"]

# Carrega o modelo de linguagem
modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Transforma o texto limpo em um vetor númerico

vetores = modelo.encode(noticias_validas['texto_limpo'].tolist())
np.save('embeddings.npy', modelo)

print(f"Embeddings gerados: {vetores.shape}")