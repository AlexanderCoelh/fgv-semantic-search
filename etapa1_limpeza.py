import pandas as pd
from bs4 import BeautifulSoup
import html
import re

df = pd.read_json("dados/noticias_brutas.json")

# Criando a Função para limpar o texto

def limpar_texto(texto):
    texto = html.unescape(texto)
    texto = re.sub(r'<p>.*?\d{2}/\d{2}/\d{4}.*?</p>', '', texto)
    soup = BeautifulSoup(texto, 'html.parser')
    texto = soup.get_text(separator='') 
    texto = re.sub(r'.*?Publicado em.*?[\n\.]', '', texto)       
    texto = re.sub(r'\d{2}/\d{2}/\d{4}.*?\d{2}h\d{2}[^\w]*', '', texto) 
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

# Aplicando a função no dataset

df['texto_limpo'] = df['texto'].apply(limpar_texto)

#Criando novas colunas e renomeando

df['validacao'] = df['texto_limpo'].str.len().apply(lambda x: 'Válido' if x > 50 else 'Inválido')
df = df.rename(columns={'data': 'data_de_publicacao'} )

#Salvando o arquivo limpo

df.to_json("dados_limpos/noticias_limpas.json", orient='records', force_ascii=False, indent=2)


print(df[['titulo', 'texto_limpo', 'validacao']].to_string())
