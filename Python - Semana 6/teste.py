
import pandas as pd
import plotly.express as px
import streamlit as st

def card_com_borda(titulo, valor):
    st.markdown(
        f"""
        <div style="
            border: 2px solid #00008B; 
            border-radius: 10px; 
            padding: 10px; 
            text-align: center; 
            background-color: #f9f9f9;">
            <h3 style="margin: 0;">{titulo}</h3>
            <p style="font-size: 24px; font-weight: bold; margin: 5px 0 0 0;">{valor}</p>
        </div>
        """, unsafe_allow_html=True
    )

def formata_brasileiro(numero):
    saida = f"{numero:_.2f}"
    saida = saida.replace('.',',').replace('_','.')
    return saida

page_bg_img = '''
<style>
    .stApp {
        background-color: #F0F0F0;
    }
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)    

# para executar é necessário identificar o caminho completo
# streamlit run "/Users/margarida/Documents/Curso Python/Educ360/repo/Educ360/Python - Semana 6/dashboard.py"

# Demanda Cliente
# 1 - Números de Consultas Geral e por Data - barra
# 2 - Por unidade as consultas - Dados - Especialidades
# layout da página

st.set_page_config(page_title="Painel de Consultas Médicas", layout="wide")

#CSV
df=pd.read_csv('/Users/margarida/Documents/Curso Python/Educ360/repo/Educ360/Python - Semana 6/consulta.csv',
               parse_dates=['dataconsulta'])

# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros")

#Combo das datas
# recebe todas as datas (df), classifica e filtra somente 1 de cada (unique)
datas_unicas = sorted(df['dataconsulta'].dt.strftime("%d-%m-%Y").unique())
#usando os recursos do st, crio uma barra lateral com as opções (selectbox) com a primeira opçao como Todas
opcao_data = st.sidebar.selectbox("Selecione a data:",options=["Todas"] + datas_unicas)

#Combo das unidades

unidades = sorted(df['unidade'].unique())
opcao_unidade = st.sidebar.selectbox("Selecione uma unidade:", options=["Todas"] + unidades)
                  
#Aplicar filtros

df_filtrado = df.copy()

if opcao_data != "Todas":
    df_filtrado = df_filtrado[df_filtrado["dataconsulta"].dt.strftime("%d-%m-%Y") == opcao_data]

if opcao_unidade != "Todas":
    df_filtrado = df_filtrado[df_filtrado["unidade"] == opcao_unidade]

# Cálculos para os cards
total_consultas = len(df_filtrado)
num_unidades = df_filtrado['unidade'].nunique()
total_faturamento = df_filtrado['valor'].sum() if 'valor' in df_filtrado.columns else 0.
total_faturamento = formata_brasileiro(total_faturamento)
    
st.markdown("---")    

# Composição dos gráficos

st.title(":blue[🩺 Painel de Consultas Médicas]")
multi = '''Explore as informações das consultas do último período. Utilize os filtros à esquerda para refinar sua análise.'''
st.markdown(multi)

fat_unidade = df_filtrado.groupby("unidade").agg({"valor": 'sum'}).reset_index()
fat_unidade.columns = ['unidade', 'valor']
titulo_grafico = "Todas" if opcao_unidade == "Todas" else opcao_unidade.capitalize()

fig3 = px.bar(
    fat_unidade,
    x = "unidade",
    y = "valor",
    color = "unidade",
    title=f"Fat. Total por unidade<br>({titulo_grafico})",
    text="valor",
    color_discrete_sequence = px.colors.qualitative.Pastel
)
fig3.update_layout(xaxis_title="Unidade(s)", yaxis_title="Faturamento (R$)")
fig3.update_layout(title_x=0.5, title_xanchor='center')
#col3.plotly_chart(fig3, use_container_width=True)
fig3.show()


