# bibliotecas
import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# configuraçao da pagina
st.set_page_config(page_title="Raspagem Aula", layout='wide')
st.title("Raspagem de Dados")

# URL - Alvo
#ler a página que deseja fazer a raspagem

url = "https://rhplay.com.br/"

#identificar o agente 
# F12 na página que deseja carregar
# cabeçalho de requisição está em Network -> Request Headers -> User-Agent
# Ou vc pode ir direto no browser
# digitar: my user agent chrome
# terá como resposta um endereço Qual é o meu agente de usuário?
# clica nele e a página vai mostrar o agente

cabecalho = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.6 Safari/605.1.15'
}

r = requests.get(url,headers=cabecalho)

#tratamento
site = BeautifulSoup(r.content,'html.parser')
# cria lista vazia
links=[]
# percorre o site procurando tudo o que começa com 'a'
for a in site.find_all('a', href=True):
    texto = a.get_text(strip=True)
    link = a['href']
    #garante que o texto tenha conteúdo
    if texto and link not in ('#','/',''):
        if link.startswith('/'):
            #remove a barra final
            link = url.rstrip('/') + link
        link = f"<a href='{link}'>{link} </a>"
        # faz o append na lista    
        links.append({'Texto do link': texto, 'URL': link})

df = pd.DataFrame(links)    
st.markdown(df.to_html(escape=False,index=False), unsafe_allow_html = True)