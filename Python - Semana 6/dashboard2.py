
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

#ajustar o conteúdo das colunas
df['tipoconsulta']= df['tipoconsulta'].str.capitalize()
df['unidade']= df['unidade'].str.capitalize()

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

#Formatar a saída do filtro
opcao_formatada = "Todas" if opcao_unidade == "Todas" else opcao_unidade.capitalize()    

# Cálculos para os cards
total_consultas = len(df_filtrado)
num_unidades = df_filtrado['unidade'].nunique()
total_faturamento = df_filtrado['valor'].sum() if 'valor' in df_filtrado.columns else 0.
total_faturamento = formata_brasileiro(total_faturamento)
    
# Exibir os cards lado a lado
card1, card2, card3 = st.columns(3)
with card1:
    card_com_borda("Total de Consultas", total_consultas)
with card2:
    card_com_borda("Unidades Ativas", num_unidades)
with card3:
    card_com_borda("Faturamento Total", f"R$ {total_faturamento}")

st.markdown("---")    

# Composição dos gráficos

st.title(":blue[🩺 Painel de Consultas Médicas]")
multi = '''Explore as informações das consultas do último período. Utilize os filtros à esquerda para refinar sua análise.'''
st.markdown(multi)
col1, col2, col3 = st.columns(3)

# Grafico 1 - Número de Consultas por Unidade

consultas_unidade = df_filtrado.groupby("unidade").size().reset_index(name="Total")

fig1 = px.bar(
    consultas_unidade,
    x = "unidade",
    y = "Total",
    color="unidade",
    title=f"Nr de Consultas por Unidades<br>({opcao_data})",
    text="Total",
    color_discrete_sequence = px.colors.qualitative.Pastel
)

fig1.update_layout(xaxis_title="Unidade(s)", yaxis_title="Total de Consultas")
fig1.update_layout(title_x=0.5, title_xanchor='center')
col1.plotly_chart(fig1, use_container_width=True)

# Grafico 2 - Consulta por Unidade x Especialidades

consulta_tipo = df_filtrado["tipoconsulta"].value_counts().reset_index(name="Total")
consulta_tipo.columns = ['tipoconsulta', 'Total']

fig2 = px.pie(
    consulta_tipo,
    names = "tipoconsulta",
    values = "Total",
    title = f"Consultas por Especialidade",
    color = "tipoconsulta",
    hole=0.3,
    color_discrete_sequence = px.colors.qualitative.Pastel
)

fig2.update_layout(title_x=0.5, title_xanchor='center')
col2.plotly_chart(fig2, use_container_width=True)

# Grafico 3 - Faturamento Total por Unidade
fat_unidade = df_filtrado.groupby("unidade").agg({"valor": 'sum'}).reset_index()
fat_unidade.columns = ['unidade', 'valor']

fig3 = px.bar(
    fat_unidade,
    x = "unidade",
    y = "valor",
    color = "unidade",
    title=f"Fat. Total por unidade<br>({opcao_formatada})",
    text="valor",
    color_discrete_sequence = px.colors.qualitative.Pastel
)
fig3.update_layout(xaxis_title="Unidade(s)", yaxis_title="Faturamento (R$)")
fig3.update_layout(title_x=0.5, title_xanchor='center')
col3.plotly_chart(fig3, use_container_width=True)

st.markdown("---")   

# Visão dos atendimentos

st.subheader(f":blue[🗃️ Registros: {opcao_unidade}]")

# Mostrar a data de retorno - ao invés da quantidade de dias
df_filtrado['data_retorno'] = df_filtrado['dataconsulta'] + pd.to_timedelta(df_filtrado['retornodaconsulta'], unit='days')
df_filtrado = df_filtrado.drop('retornodaconsulta', axis=1)

# Formatar o valor para apresentar virgula no lugar do ponto
df_filtrado['valor_formatado'] = df_filtrado['valor'].apply(formata_brasileiro) 
df_filtrado = df_filtrado.drop('valor', axis=1)


coluna_formatada = {
    'dataconsulta': st.column_config.DateColumn("Data Consulta", format='DD/MM/YYYY'),
    'unidade': st.column_config.TextColumn("Unidade"),
    'tipoconsulta': st.column_config.TextColumn("Especialidade"),
    'valor_formatado': st.column_config.TextColumn("Valor (R$)"),
    'data_retorno': st.column_config.DateColumn("Data retorno", format='DD/MM/YYYY')

}
st.dataframe(df_filtrado, column_config=coluna_formatada, use_container_width= True)
