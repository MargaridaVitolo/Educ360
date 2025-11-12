
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import base64
from pathlib import Path 
from thefuzz import process, fuzz
import io


#streamlit run "/Users/margarida/Documents/Curso Python/Educ360/repo/Educ360/AtlanticoDigital/Atlantico.py"

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

# --- 1. Função para Obter o Base64 da Imagem ---
def img_to_base64(img_path):
    """Lê um arquivo de imagem e retorna sua string codificada em Base64."""
    try:
        # Abre o arquivo em modo binário ('rb')
        with open(img_path, "rb") as img_file:
            # Codifica os dados binários para Base64
            b64_string = base64.b64encode(img_file.read()).decode()
        return b64_string
    except FileNotFoundError:
        st.error(f"Erro: Arquivo '{img_path}' não encontrado.")
        return None

page_bg_img = '''
<style>
    .stApp {
        background-color: #F0F0F0;
    }
</style>
'''

# Define o caminho do GIF relativo ao arquivo atual
gif_filename = Path(__file__).parent / "Atlantico.gif"

#-------------------------------------------------------------------

st.markdown(page_bg_img, unsafe_allow_html=True)    

st.set_page_config(page_title="Atlântico Digital", layout="wide")

#-------------------------------------------------------------------
# UPLOAD ARQUIVO
#-------------------------------------------------------------------

# --- Barra Lateral (Upload Excel e Filtros) ---
st.sidebar.header("📂 Upload do arquivo Excel")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo Excel", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        # df['data_venda'] = pd.to_datetime(df['data_venda'])
        st.sidebar.success("Arquivo Excel carregado com sucesso!")
        
    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo Excel: {e}")
        st.stop()
        
else:
    st.sidebar.warning("Por favor, envie um arquivo Excel para análise.")
    st.stop()

st.sidebar.header("🔍 Filtros para Análise")

#-------------------------------------------------------------------
# LIMPEZA ARQUIVO
#-------------------------------------------------------------------



#-------------------------------------------------------------------
#Combo de quadros
#-------------------------------------------------------------------

quadros = sorted(df['Quadro'].unique())
opcao_quadros = st.sidebar.selectbox("Selecione um Quadro:", options=["Todos"] + quadros)

#-------------------------------------------------------------------
#Combo de grupos
#-------------------------------------------------------------------

grupos = sorted(df['Grupo'].dropna().unique())
opcao_grupos = st.sidebar.selectbox("Selecione um Grupo:", options=["Todos"] + grupos)

#-------------------------------------------------------------------
#Combo de projetos
#-------------------------------------------------------------------

#ajuste dos nomes dos projetos

projeto_correta = ["Atlântico Essencial", "OPERACOES", "SAVE"]
LIMIAR_AJUSTE = 75
projetos = sorted(df['Projeto'].unique())
projetos_corrigida=[]

# Criar um dicionário de mapeamento entre nome original e nome corrigido
mapa_correcao = {}

for palavra in projetos:
    best_match = process.extractOne(palavra, projeto_correta)
    if best_match and best_match[1] >= LIMIAR_AJUSTE:
        palavra_corrigida = best_match[0]
    else:
        palavra_corrigida = palavra  # mantém o nome original se não encontrou correspondência boa

    # guarda o resultado
    projetos_corrigida.append(palavra_corrigida)
    mapa_correcao[palavra] = palavra_corrigida  # cria o mapeamento original → corrigido

# Atualiza o DataFrame com as correções
df['Projeto'] = df['Projeto'].map(mapa_correcao)

# Elimina duplicatas e ordena
projetos_corrigida = sorted(set(projetos_corrigida))

# Gera o combo de seleção
opcao_projetos = st.sidebar.selectbox("Selecione um Projeto:", options=["Todos"] + projetos_corrigida)

#-------------------------------------------------------------------
#Combo de clientes
#-------------------------------------------------------------------

clientes = sorted(df['Cliente'].unique())
opcao_clientes = st.sidebar.selectbox("Selecione um Cliente:", options=["Todos"] + clientes)

#-------------------------------------------------------------------
# --- Filtro de datas com ícone de calendário 🗓️ ---
#-------------------------------------------------------------------

# Garante que a coluna de datas está no formato datetime
df['Criada em'] = pd.to_datetime(df['Criada em'], errors='coerce')

# Define data mínima e máxima automaticamente
data_min = df['Criada em'].min().date()
data_max = df['Criada em'].max().date()

# --- Seletor de data inicial ---
data_inicial = st.sidebar.date_input(
    "📅 Data Inicial:",
    value=data_min,
    min_value=data_min,
    max_value=data_max
)

# --- Seletor de data final ---
data_final = st.sidebar.date_input(
    "📅 Data Final:",
    value=data_max,
    min_value=data_min,
    max_value=data_max
)

# Garantir que data_final nunca seja menor que data_inicial
if data_final < data_inicial:
    st.sidebar.warning("⚠️ A data final não pode ser anterior à data inicial. Ajustando automaticamente.")
    data_final = data_inicial

# --- Top N resultados ---
st.sidebar.header("⚙️ Configurações de Exibição")

top_n = st.sidebar.number_input(
    "Número de registros a exibir nos gráficos (Top N):",
    min_value=3,
    max_value=50,
    value=10,
    step=1,
    help="Define quantos registros serão mostrados nos gráficos (ex: Top 10 tarefas, pessoas, etc.)"
)

#-------------------------------------------------------------------
#Aplicar filtros
#-------------------------------------------------------------------

df_filtrado = df.copy()

if opcao_quadros != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Quadro"] == opcao_quadros]

if opcao_grupos != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Grupo"] == opcao_grupos]    

if opcao_projetos != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Projeto"] == opcao_projetos]

if opcao_clientes != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Cliente"] == opcao_clientes]

# Filtra o DataFrame conforme o intervalo de datas selecionado
df_filtrado = df_filtrado[
    (df_filtrado['Criada em'].dt.date >= data_inicial) &
    (df_filtrado['Criada em'].dt.date <= data_final)
]    

#-------------------------------------------------------------------
# principal
#-------------------------------------------------------------------

# Nome do seu arquivo GIF (deve estar na mesma pasta do script)
gif_filename = '/Users/margarida/Documents/Curso Python/Educ360/repo/Educ360/AtlanticoDigital/Atlantico.gif'

# Converte o GIF e obtém a string Base64
base64_gif = img_to_base64(gif_filename)

if base64_gif:
    # Cria o URI de dados no formato HTML: data:image/gif;base64,...
    # O MIME type para GIF é image/gif
    gif_uri = f"data:image/gif;base64,{base64_gif}"

GIF_WIDTH = 50

st.markdown(
        f"""
        <div style='display: flex; align-items: center;'>
            <img src='{gif_uri}' width='{GIF_WIDTH}' style='vertical-align: middle;'>
            <h1 style='color:#0A4D8C; margin-right: 10px;'>&nbsp;&nbsp;Atlântico Digital</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
#-------------------------------------------------------------------
# CARDS
#-------------------------------------------------------------------


# Cálculos para os cards
total_tarefas = df_filtrado['ID da Tarefa'].count()
total_encerradas = df_filtrado['Fase'].value_counts().get('Entregue',0)

df_filtrado['Criada em'] = pd.to_datetime(df_filtrado['Criada em'])
df_filtrado['Fechada em'] = pd.to_datetime(df_filtrado['Fechada em'])
df_filtrado['Dias_para_fechamento'] = (df_filtrado['Fechada em'] - df_filtrado['Criada em']).dt.days
media_dias = round(df_filtrado['Dias_para_fechamento'].mean(),1)


# Verificar se não há dados
if total_tarefas == 0:
    st.warning("⚠️ Não existem dados que atendam aos filtros selecionados.")
    st.stop()

# Exibir os cards lado a lado
card1, card2, card3 = st.columns(3)
with card1:
    card_com_borda("Total tarefas", total_tarefas)
with card2:
    card_com_borda("Encerradas no Período", total_encerradas)
with card3:
    card_com_borda("SLA Medio (dias)", media_dias)

st.markdown("---")  

#-------------------------------------------------------------------
# Composição dos gráficos
#-------------------------------------------------------------------

st.subheader(":blue[📈 Análise Período]")
multi = '''Explore as informações do último período. Utilize os filtros à esquerda para refinar sua análise.'''
st.markdown(multi)
l1_col1, l1_col2 = st.columns(2)
l2_col1, l2_col2 = st.columns(2)

# Grafico 1 - Média de dias para fechamento por tipo de tarefa

# Diferença em dias
df_filtrado['Dias_para_fechamento'] = (df_filtrado['Fechada em'] - df_filtrado['Criada em']).dt.days

# Total de tarefas por tipo
total_tarefas = df_filtrado.groupby('Tipo de tarefa').size().reset_index(name='Total_Tarefas')

# Média de dias por tipo
media_dias = df_filtrado.groupby('Tipo de tarefa')['Dias_para_fechamento'].mean().reset_index()
media_dias = media_dias.round(1)

# Combinar as métricas em um único DataFrame
df_grafico = pd.merge(total_tarefas, media_dias, on='Tipo de tarefa')

# --- Selecionar top 10 pelo total de tarefas ---
df_grafico = df_grafico.sort_values(by='Total_Tarefas', ascending=False).head(top_n)

# --- Criar gráfico combinado ---
fig1 = go.Figure()

# Barras: total de tarefas
fig1.add_trace(go.Bar(
    x=df_grafico['Tipo de tarefa'],
    y=df_grafico['Total_Tarefas'],
    name='Total de Tarefas',
    text=df_grafico['Total_Tarefas'],
    textposition='outside',
    yaxis='y1'
))

# Linha: média de dias
fig1.add_trace(go.Scatter(
    x=df_grafico['Tipo de tarefa'],
    y=df_grafico['Dias_para_fechamento'],
    name='Média de Dias',
    mode='lines+markers+text',
    text=df_grafico['Dias_para_fechamento'],
    textfont=dict(color='black'),
    textposition='top center',
    marker=dict(color='orange', size=10),
    yaxis='y2'
))

# --- Layout ---
fig1.update_layout(
    title=dict(
        text=f'Total de Tarefas e SLA Médio de Encerramento <br>' 
             f'<span style="font-size:16px;">(Somente as {top_n} primeiras tarefas mais executadas)</span>'),
    title_x=0.5,
    xaxis_title='Tipo de Tarefa',
    yaxis=dict(
        title='Total de Tarefas',
        showgrid=False,
        zeroline=False
    ),
    yaxis2=dict(
        title='Média de Dias',
        overlaying='y',
        side='right',
        showgrid=False,
        zeroline=False
    ),
    legend=dict(x=0.9, y=1.0),
    barmode='group',
    template='plotly_white',
    #width=1200,
    height=600
)

fig1.update_layout(
    title=dict(
        #text='',
        #x=0.5, 
        xanchor='center',
        font=dict(
            size=20,
            color='#0A4D8C',
            family="Calibri"
        )
    )
)
l1_col1.plotly_chart(
    fig1,
    config={"responsive": True},  # substitui use_container_width
)

# Grafico 2 - Média de dias para fechamento por urgencia

# Agrupar por Urgente e calcular contagem + média
df_urgente = (
    df_filtrado.groupby('Urgente')
    .agg(
        Total_Tarefas=('ID da Tarefa', 'count'),
        Media_Dias=('Dias_para_fechamento', 'mean')
    )
    .reset_index()
)
df_urgente['Media_Dias'] = df_urgente['Media_Dias'].round(1)


fig2= px.pie(
    df_urgente,
    names='Urgente',
    values='Total_Tarefas',
    title='Distribuição de Tarefas por Urgência e SLA Médio',
    color='Urgente',
    color_discrete_sequence = px.colors.qualitative.Pastel,
    hole=0.3,  # Faz o gráfico ser tipo donut (opcional)
    custom_data=['Media_Dias']
)

# Adiciona labels com o valor de dias
fig2.update_traces(
    texttemplate="%{label}<br>%{value} tarefas<br>⏱️ %{customdata[0]} dias médios",
    textposition='inside',
    textfont=dict(
        size=14,
        color='black',
        family='Calibri'
    )
)

# --- Forçar mesmo tamanho e estilo visual do gráfico 1 ---
fig2.update_layout(
    height=600,  # mesma altura do grafico1
    title=dict(
        x=0.5,
        xanchor='center',
        font=dict(
            size=20,
            color='#0A4D8C',
            family="Calibri"
        )
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.15,
        xanchor="center",
        x=0.5
    ),
    template='plotly_white'
)

# Exibe no Streamlit
l1_col2.plotly_chart(fig2, use_container_width=True)

# ======================================================
# 📊 Gráfico - Alocação de tarefas por equipe
# ======================================================

# Garante que temos a coluna de diferença em dias
df_filtrado['Dias_para_fechamento'] = (df_filtrado['Fechada em'] - df_filtrado['Criada em']).dt.days

# Agrupar por equipe
df_equipes = (
    df_filtrado.groupby('Equipe')
    .agg(
        Total_Tarefas=('ID da Tarefa', 'count'),
        Media_Dias=('Dias_para_fechamento', 'mean')
    )
    .reset_index()
)

# Arredondar valores
df_equipes['Media_Dias'] = df_equipes['Media_Dias'].round(1)

# Ordenar pelo total de tarefas (decrescente)
df_equipes = df_equipes.sort_values(by='Total_Tarefas', ascending=False)

# Criar gráfico combinado
fig3 = go.Figure()

# --- Barras: Total de tarefas ---
fig3.add_trace(go.Bar(
    x=df_equipes['Equipe'],
    y=df_equipes['Total_Tarefas'],
    name='Total de Tarefas',
    text=df_equipes['Total_Tarefas'],
    textposition='outside',
    marker_color='#5DADE2',
    yaxis='y1'
))

# --- Linha: Média de dias ---
fig3.add_trace(go.Scatter(
    x=df_equipes['Equipe'],
    y=df_equipes['Media_Dias'],
    name='Média de Dias para Encerramento',
    mode='lines+markers+text',
    text=df_equipes['Media_Dias'],
    textfont=dict(color='black', family='Calibri', size=12),
    textposition='top center',
    marker=dict(color='orange', size=10),
    line=dict(color='orange', width=2),
    yaxis='y2'
))

# --- Layout ---
fig3.update_layout(
    title=dict(
        text=f'Alocação de Tarefas por Equipe',
        x=0.3,
        font=dict(size=20, color='#0A4D8C', family='Calibri')
    ),
    xaxis_title='Time Responsável',
    yaxis=dict(
        title='Total de Tarefas',
        showgrid=False,
        zeroline=False
    ),
    yaxis2=dict(
        title='Média de Dias',
        overlaying='y',
        side='right',
        showgrid=False,
        zeroline=False
    ),
    legend=dict(x=0.85, y=1.1),
    barmode='group',
    template='plotly_white',
    height=800
)

# --- Exibir no Streamlit ---
l2_col1.plotly_chart(fig3, config={"responsive": True})

#-------------------------------------------------------------------
# GRAFICO 4 - Tarefas com maior atraso
#-------------------------------------------------------------------

# Converter colunas para datetime
df_filtrado['Criada em'] = pd.to_datetime(df_filtrado['Criada em'], errors='coerce')
df_filtrado['Entrega desejada'] = pd.to_datetime(df_filtrado['Entrega desejada'], errors='coerce')
df_filtrado['Fechada em'] = pd.to_datetime(df_filtrado['Fechada em'], errors='coerce')

# Calcular atraso em dias (para tarefas fechadas)
df_filtrado['Atraso_dias'] = (df_filtrado['Fechada em'] - df_filtrado['Entrega desejada']).dt.days

# Para tarefas ainda abertas (sem "Fechada em"), calcular atraso até hoje
df_filtrado.loc[df_filtrado['Fechada em'].isna(), 'Atraso_dias'] = (
    (pd.Timestamp.today() - df_filtrado['Entrega desejada']).dt.days
)

# Filtrar somente as tarefas atrasadas (dias > 0)
df_atrasadas = df_filtrado[df_filtrado['Atraso_dias'] > 0].copy()

# Criar coluna de status visual
df_atrasadas['Status_Atraso'] = df_atrasadas['Fechada em'].apply(
    lambda x: 'Encerrada' if pd.notnull(x) else 'Atrasada em Andamento'
)

# -------------------------------
# 📊 Cálculos para o resumo
# -------------------------------
total_atrasadas = df_atrasadas.shape[0]
media_atraso = round(df_atrasadas['Atraso_dias'].mean(), 1)

# -------------------------------
# 🔻 Gráfico de Atrasos por Tipo de Tarefa
# -------------------------------

# 🔹 Agrupar dados por tipo de tarefa e status
df_atraso_tipo = (
    df_atrasadas
    .groupby(['Tipo de tarefa', 'Status_Atraso'])
    .agg(
        Total_Tarefas=('ID da Tarefa', 'count'),
        Media_Atraso=('Atraso_dias', 'mean')
    )
    .reset_index()
)

# Arredonda os valores
df_atraso_tipo['Media_Atraso'] = df_atraso_tipo['Media_Atraso'].round(1)

# Ordenar pelo maior atraso médio
df_atraso_tipo = df_atraso_tipo.sort_values(by='Media_Atraso', ascending=False)

# 🔹 Criar gráfico de barras horizontais
fig4 = go.Figure()

# Adiciona uma barra por status (Encerrada / Atrasada em Andamento)
for status, cor in zip(['Encerrada', 'Atrasada em Andamento'], ['#FF4D4D', '#FFA500']):
    subset = df_atraso_tipo[df_atraso_tipo['Status_Atraso'] == status]
    fig4.add_trace(go.Bar(
        y=subset['Tipo de tarefa'],             # eixo Y = tipo de tarefa
        x=subset['Media_Atraso'],               # eixo X = média de atraso em dias
        name=f"{status}",
        marker_color=cor,
        text=subset['Media_Atraso'],
        texttemplate='%{text} dias',
        textposition='outside',
        orientation='h'                         # barras horizontais
    ))

# 🔹 Layout do gráfico
fig4.update_layout(
    title=dict(
        text=f"Média de Dias de Atraso por Tipo de Tarefa",
        x=0.2,
        font=dict(size=20, color='#0A4D8C', family='Calibri')
    ),
    yaxis_title='Tipo de Tarefa',
    xaxis_title='Média de Dias de Atraso',
    barmode='group',  # barras lado a lado
    template='plotly_white',
    height=600,
    font=dict(family='Calibri', color='#0A4D8C', size=14),
    legend_title_text='Status',
    legend=dict(x=0.7, y=1.05, orientation='h')
)

# -------------------------------
# Exibir gráfico e cards dentro do mesmo container
# -------------------------------
with l2_col2:
    st.plotly_chart(fig4, use_container_width=True)

    # Pequeno espaçamento entre gráfico e cards
    st.markdown("<br>", unsafe_allow_html=True)

    # Cards dentro da mesma coluna
    c1, c2 = st.columns(2)
    with c1:
        card_com_borda("📦 Atrasadas", total_atrasadas)
    with c2:
        card_com_borda("⏱️ Média Atraso", f"{media_atraso} dias")

  
#-------------------------------------------------------------------
# DATAFRAME FILTRADO
#-------------------------------------------------------------------

# --- Exibe o intervalo de datas selecionado no topo ---
data_inicial_fmt = data_inicial.strftime("%d/%m/%Y")
data_final_fmt = data_final.strftime("%d/%m/%Y")

st.markdown(
    f"""
    <div style='background-color:#E6F0FA; padding:10px; border-radius:8px; margin-top:15px;'>
        <h4 style='color:#0A4D8C; margin:0;'>
            📅 <b>Período selecionado:</b> {data_inicial_fmt} → {data_final_fmt}
        </h4>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Formata a coluna de data no padrão brasileiro (dd/mm/aaaa) ---
if 'Criada em' in df_filtrado.columns:
    df_filtrado['Criada em'] = df_filtrado['Criada em'].dt.strftime("%d/%m/%Y")

# --- Exibe o DataFrame filtrado ---
st.dataframe(df_filtrado, use_container_width=True)
st.write(f"🔎 Total de registros filtrados: **{len(df_filtrado)}**")

# --- Botão para download do DataFrame filtrado ---

# Converte o DataFrame filtrado para Excel em memória
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df_filtrado.to_excel(writer, index=False, sheet_name='Dados Filtrados')

# Obtém os bytes do arquivo Excel gerado
dados_excel = output.getvalue()

# Botão de download 
st.download_button(
    label="📥 Baixar Excel filtrado",
    data=dados_excel,
    file_name=f"Dados_Filtrados_{data_inicial}_a_{data_final}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    key="download_button"
)

st.markdown("</div>", unsafe_allow_html=True)

