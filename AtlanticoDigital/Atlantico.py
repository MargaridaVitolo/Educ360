
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import base64
import io
import os
from pathlib import Path 
from thefuzz import process, fuzz
from datetime import datetime


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
    """
    Lê um arquivo de imagem e retorna sua string codificada em Base64.
    Se o arquivo não existir, retorna None e exibe um aviso.
    """
    img_path = Path(img_path)
    if not img_path.exists():
        st.warning(f"⚠️ Imagem não encontrada: {img_path}")
        return None
    
    with open(img_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return b64_string

def decimal_para_hora_min(decimal_horas):
    #horas = int(decimal_horas)  # parte inteira = horas
    #minutos = int(round((decimal_horas - horas) * 60))  # parte decimal convertida em minutos arredondados
    if pd.isna(decimal_horas) or decimal_horas is None:
        return '00:00'
    
    # Total de minutos
    total_minutos = int(round(decimal_horas * 60))
    
    # Extrair horas e minutos
    horas = total_minutos // 60
    minutos = total_minutos % 60
    
    return f"{horas:02d}:{minutos:02d}"


def explode_dados(df):
    df = df.copy()
    df['equipe'] = df['equipe'].fillna("").astype(str)
    df['lista'] = df['equipe'].apply(lambda x: [p.strip() for p in x.split(",") if p.strip()])
    df = df.explode('lista')
    df['equipe_resp'] = df['lista']
    return df.drop(columns=['lista'])

page_bg_img = '''
<style>
    .stApp {
        background-color: #F0F0F0;
    }
</style>
'''

#-------------------------------------------------------------------

st.markdown(page_bg_img, unsafe_allow_html=True)    

st.set_page_config(page_title="Atlântico Digital", layout="wide")

#-------------------------------------------------------------------
# UPLOAD ARQUIVO
#-------------------------------------------------------------------

# --- Barra Lateral (Upload Excel e Filtros) ---
st.sidebar.header("📂 Upload do arquivo")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo (Excel,CSV)", type=['xlsx', 'xls','csv'])

if uploaded_file is not None:
    # Captura o nome do arquivo
    file_name = uploaded_file.name
    # Extrai a extensão do arquivo
    file_ext = os.path.splitext(file_name)[1].lower()  # .csv, .xlsx, .xls

    try:
        if file_ext == '.csv':
            df = pd.read_csv(uploaded_file,sep=';',usecols=(0,1,2,3,6,7,9,10,15,16,18,19,21,23,25,26))
            st.sidebar.success("Arquivo CSV carregado com sucesso!")
        elif file_ext in ['.xls', '.xlsx']:
            df = pd.read_excel(uploaded_file,usecols=(0,1,2,3,6,7,9,10,15,16,18,19,21,23,25,26))
            st.sidebar.success("Arquivo Excel carregado com sucesso!")
        else:
            st.sidebar.error("Tipo de arquivo não suportado.")
            st.stop()
    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo: {e}")
        st.stop()
else:
    st.sidebar.warning("Por favor, envie um arquivo Excel ou CSV para análise.")
    st.stop()

st.sidebar.divider() 

#-------------------------------------------------------------------
# NOMEAR AS COLUNAS 
#-------------------------------------------------------------------

# Ajustar os nomes das colunas com um nome interno

novos_nomes = [
'quadro',
'cliente',
'grupo',
'projeto',
'tipo_tarefa',
'equipe',
'para',
'id_tarefa',
'dt_abertura',
'dt_entrega_desejada',
'dt_fechada',
'esforco_estimado',
'esforco_registrado',
'percentual_realizado',
'fase',
'st_reaberta'
]

df.columns = novos_nomes

#-------------------------------------------------------------------
# LIMPEZA ARQUIVO
#-------------------------------------------------------------------

df['equipe'] = df['equipe'].fillna("Não Informado").replace("", "Não Informado")

#-------------------------------------------------------------------
# SELEÇÃO DOS RELATÓRIOS A APRESENTAR
#-------------------------------------------------------------------

relatorios = [
    "Tarefas Reabertas",
    "SLA",
    "Tempo médio por Tarefas",
    "Tempo médio por Clientes"
]

selecoes = {}

st.sidebar.header("Selecione os relatórios para visualizar:")

# Criar um checkbox para cada relatório, armazenando a seleção no dicionário
for relatorio in relatorios:
    selecoes[relatorio] = st.sidebar.checkbox(relatorio, value=False)  # Inicialmente desmarcado

# Exemplo de uso: mostrar quais relatórios foram selecionados
relatorios_selecionados = [r for r, selecionado in selecoes.items() if selecionado]

st.sidebar.divider() 

#-------------------------------------------------------------------
#Combo de quadros
#-------------------------------------------------------------------

quadros = sorted(df['quadro'].unique())

#-------------------------------------------------------------------
#Combo de grupos
#-------------------------------------------------------------------

grupos = sorted(df['grupo'].dropna().unique())

#-------------------------------------------------------------------
#Combo de projetos
#-------------------------------------------------------------------

#ajuste dos nomes dos projetos

projeto_correta = ["Atlântico Essencial", "OPERACOES", "SAVE"]
LIMIAR_AJUSTE = 75
projetos = sorted(df['projeto'].unique())
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
df['projeto'] = df['projeto'].map(mapa_correcao)

# Elimina duplicatas e ordena
projetos_corrigida = sorted(set(projetos_corrigida))

#-------------------------------------------------------------------
#Combo de clientes
#-------------------------------------------------------------------

clientes = sorted(df['cliente'].unique())

#-------------------------------------------------------------------
#Combo de tarefas
#-------------------------------------------------------------------

tarefas = sorted(df['tipo_tarefa'].unique())

#-------------------------------------------------------------------
# APRESENTA OPÇÃO PARA O USUÁRIO FILTRAR OS DADOS
#-------------------------------------------------------------------

df_filtrado = df.copy()

st.sidebar.header("🔍 Filtros para Análise")

# Checkbox para o usuário escolher se quer filtrar os dados
filtrar_dados = st.sidebar.checkbox("Deseja filtrar os dados dos relatórios?")

if filtrar_dados:
    opcao_quadros    = st.sidebar.selectbox("Selecione um Quadro:",  options=["Todos"] + quadros)
    opcao_grupos     = st.sidebar.selectbox("Selecione um Grupo:",   options=["Todos"] + grupos)
    opcao_projetos   = st.sidebar.selectbox("Selecione um Projeto:", options=["Todos"] + projetos_corrigida)
    opcao_clientes   = st.sidebar.selectbox("Selecione um Cliente:", options=["Todos"] + clientes)
    opcao_tarefas    = st.sidebar.selectbox("Selecione uma Tarefa:", options=["Todas"] + tarefas)
    mostrar_fechadas = st.sidebar.checkbox("Mostrar somente tarefas encerradas?")

    # Aplicar os filtros no DataFrame depois, conforme as escolhas do usuário
    if opcao_quadros != "Todos":
        df_filtrado = df_filtrado[df_filtrado['quadro'] == opcao_quadros]
    if opcao_grupos != "Todos":
        df_filtrado = df_filtrado[df_filtrado['grupo'] == opcao_grupos]
    if opcao_projetos != "Todos":
        df_filtrado = df_filtrado[df_filtrado['projeto'] == opcao_projetos]
    if opcao_clientes != "Todos":
        df_filtrado = df_filtrado[df_filtrado['cliente'] == opcao_clientes]
    if opcao_tarefas != "Todas":
        df_filtrado = df_filtrado[df_filtrado['tipo_tarefa'] == opcao_tarefas]   
    if mostrar_fechadas:
        df_filtrado = df_filtrado[df_filtrado['dt_fechada'].notna()]
else:
    st.sidebar.info("Nenhum filtro aplicado nos relatórios.")

#-------------------------------------------------------------------
# MOSTRAR O FILTRO DE DATAS, CASO TENHA SELECIONADO A OPÇÃO ANTERIOR
#-------------------------------------------------------------------

if filtrar_dados and mostrar_fechadas:

    # Garante que a coluna de datas está no formato datetime
    df_filtrado['dt_fechada'] = pd.to_datetime(df_filtrado['dt_fechada'], errors='coerce')

    # Define data mínima e máxima automaticamente
    data_min = df_filtrado['dt_fechada'].min().date()
    data_max = df_filtrado['dt_fechada'].max().date()    

    # --- Seletor de data inicial ---
    data_inicial = st.sidebar.date_input(
        "📅 Data Encerramento Inicial:",
        value=data_min,
        min_value=data_min,
        max_value=data_max
    )

    # --- Seletor de data final ---
    data_final = st.sidebar.date_input(
        "📅 Data Encerramento Final:",
        value=data_max,
        min_value=data_min,
        max_value=data_max
    )

    # Garantir que data_final nunca seja menor que data_inicial
    if data_final < data_inicial:
        st.sidebar.warning("⚠️ A data final não pode ser anterior à data inicial.")
        data_final = data_inicial

    # Filtra o DataFrame conforme o intervalo de datas selecionado
    df_filtrado = df_filtrado[
        (df_filtrado['dt_fechada'].dt.date >= data_inicial) &
        (df_filtrado['dt_fechada'].dt.date <= data_final)
    ]           

#-------------------------------------------------------------------
# MOSTRAR OPCAO PARA REDUZIR O NÚMERO DE INFORMAÇOES APRESENTADAS
#-------------------------------------------------------------------

# --- Top N resultados ---
st.sidebar.header("✂️ Configurações de Exibição")

top_n = st.sidebar.number_input(
    "Número de ocorrências que serão exibidas nos gráficos (Top N):",
    min_value=3,
    max_value=50,
    value=10,
    step=1,
    help="Define quantas ocorrências serão mostrados nos gráficos (ex: Top 10 tarefas, pessoas, etc.)"
)    


#-------------------------------------------------------------------
# LOGO
#-------------------------------------------------------------------

# Define o caminho do GIF relativo ao arquivo atual
gif_filename = Path(__file__).parent / "Atlantico.gif"

# Converte o GIF e obtém a string Base64
base64_gif = img_to_base64(gif_filename)

GIF_WIDTH = 50

if base64_gif:
    gif_uri = f"data:image/gif;base64,{base64_gif}"
    st.markdown(
        f"""
        <div style='display: flex; align-items: center;'>
            <img src='{gif_uri}' width='{GIF_WIDTH}' style='vertical-align: middle; margin-right: 10px;'>
            <h1 style='color:#0A4D8C; margin: 0;'>Atlântico Digital</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<h1 style='color:#0A4D8C;'>Atlântico Digital</h1>",
        unsafe_allow_html=True
    )

#-------------------------------------------------------------------
# CARDS
#-------------------------------------------------------------------

# Converter "esforco_registrado" para número (corrigindo vírgula → ponto)
df_filtrado['esforco_registrado'] = (
    df_filtrado['esforco_registrado']
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.replace(" ", "")              # remove espaços
    .replace("", "0")                  # valores vazios viram zero
    .astype(float)
)

# Criar coluna com esforço em hh:mm
df_filtrado['hora_min'] = df_filtrado['esforco_registrado'].apply(decimal_para_hora_min)

# Total de tarefas filtradas
total_tarefas = df_filtrado['id_tarefa'].count()

# Total encerradas
total_encerradas = df_filtrado['fase'].value_counts().get('Entregue', 0)

# Média de esforço em horas (decimal)
media_horas_decimal = df_filtrado['esforco_registrado'].mean()

# Converter média para HH:MM
media_horas = decimal_para_hora_min(media_horas_decimal) if pd.notna(media_horas_decimal) else "00:00"

df_filtrado['media_horas_decimal'] = media_horas_decimal

# 🔒 Validação: caso não existam dados filtrados
if total_tarefas == 0:
    st.warning("⚠️ Não existem dados que atendam aos filtros selecionados.")
    st.stop()

# Exibir os cards lado a lado
card1, card2, card3 = st.columns(3)
with card1:
    card_com_borda("Total Ocorrências", total_tarefas)
with card2:
    card_com_borda("Encerradas no Período", total_encerradas)
with card3:
    card_com_borda("SLA Médio (hh:mm)", media_horas)

#verifica qual a data minima e máxima do dataframe filtrado
data_min = df_filtrado['dt_fechada'].min().date()
data_max = df_filtrado['dt_fechada'].max().date()    

data_min_str = data_min.strftime('%d/%m/%Y') if hasattr(data_min, 'strftime') else str(data_min)
data_max_str = data_max.strftime('%d/%m/%Y') if hasattr(data_max, 'strftime') else str(data_max)

periodo_texto = f"Fechadas entre: {data_min_str} e {data_max_str}"

st.markdown(
    f"""
    <div style="color: #0A4D8C; font-size: 1.3em; margin-top: 12px;">
        {periodo_texto}
    </div>
    """, 
    unsafe_allow_html=True
)  

st.markdown("---")

# ===================================================================
# 📊 Grafico 1 - Quantidade de tarefas Reabertas e equipe responsavel
# ===================================================================
if selecoes.get("Tarefas Reabertas"):

    st.subheader(":blue[📈 Análise Tarefas Reabertas]")
    multi = '''Explore as informações do período. Utilize os filtros à esquerda para refinar sua análise.'''
    st.markdown(multi)
    
    df_explode_dados = explode_dados(df_filtrado)
    df_reabertas_sim = df_explode_dados[df_explode_dados['st_reaberta'] == 'Sim']

    df_reabertas = df_explode_dados['st_reaberta'].value_counts().reset_index()
    df_reabertas.columns = ['Status', 'Quantidade']

    fig1= px.pie(
        df_reabertas,
        names='Status',
        values='Quantidade',
        title='Percentual de Tarefas Reabertas <br> (Distribuído por equipes)',
        color='Status',
        color_discrete_sequence = px.colors.qualitative.Pastel,
        hole=0.3,  # Faz o gráfico ser tipo donut (opcional)
    )

    # --- Formatar tamanho
    fig1.update_layout(
        height=350,  
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
            y=-0.20,
            xanchor="left",
            x=0.5
        ),
        template='plotly_white'
    )    
  
    # card1 (Total Tarefas) terá 2/5 do espaço
    # coluna_titulo (para o texto único) terá os 3/5 restantes
    card1, coluna_titulo = st.columns([2, 3])
    # Card1 com total de Tarefas Reabertas
    tarefas_reabertas = df_reabertas_sim['id_tarefa'].count()
    with card1:
        card_com_borda("📦 Tarefas Reabertas <br> <br> (Distribuído por equipes)", tarefas_reabertas)

    with coluna_titulo:   
        st.plotly_chart(fig1, use_container_width=True)

    st.markdown("---")    

    # Converter todas as colunas numéricas candidatas
    colunas_numericas = ['esforco_estimado', 'id_tarefa']  
    for col in colunas_numericas:
        if col in df_reabertas_sim.columns:
            df_reabertas_sim[col] = pd.to_numeric(df_reabertas_sim[col], errors='coerce')

    df_analise = df_reabertas_sim.groupby('equipe_resp').agg(
        total_reabertas=('id_tarefa', 'count'),
        media_esforco=('esforco_estimado', 'mean')
    ).reset_index() 

    #Remove linhas com 'media_esforco' nula ou NaN
    df_analise = df_analise.dropna(subset=['media_esforco'])
    
    df_analise['media_esforco_formatada'] = df_analise['media_esforco'].apply(decimal_para_hora_min)

    # Ordena para melhor visualização (por total_reabertas decrescente) e filtra o nr de retorno top n
    df_analise = df_analise.sort_values(by=['total_reabertas', 'media_esforco_formatada'], ascending=False).head(top_n)  

    fig2 = go.Figure()
    
    # Gráfico de Barras Verticais (Tarefas Reabertas - Eixo Y Primário)
    fig2.add_trace(go.Bar(
        x=df_analise['equipe_resp'],
        y=df_analise['total_reabertas'],
        name='Tarefas Reabertas',
        marker_color='#5B84B1', 
        text=df_analise['total_reabertas'].astype(str),  # Texto a ser exibido
        textposition='outside',  # Posição: acima das barras
        textfont=dict(size=12, color='#0A4D8C'),  # Formatação do texto        
        hovertemplate="Equipe: %{x}<br>Tarefas Reabertas: %{y}<extra></extra>"
    ))

    # Gráfico de Linha (Tempo Médio de Resolução - Eixo Y Secundário)
    fig2.add_trace(go.Scatter(
        x=df_analise['equipe_resp'],
        y=df_analise['media_esforco'],
        name='Tempo Médio Resolução (Horas)',
        mode='lines+markers+text',
        marker=dict(color='#FC766A', size=10),
        line=dict(color='#FC766A', width=3),
        yaxis='y2', # Atribui ao eixo Y secundário
        text=df_analise['media_esforco_formatada'],  # ✅ Texto formatado (hh:mm)
        textposition='bottom center',  # ✅ Abaixo do marker
        textfont=dict(size=11, color='#FC766A'),  # Formatação do texto
        customdata=df_analise['media_esforco_formatada'], 
        hovertemplate="Equipe: %{x}<br>Tempo Médio: %{customdata}<extra></extra>" 
    ))

    # Gerar os valores para os ticks (rótulos) do eixo Y secundário
    # Vamos usar os valores decimais originais como tickvals e os valores formatados como ticktext
    tick_values = df_analise['media_esforco'].tolist()
    tick_text_formatted = df_analise['media_esforco_formatada'].tolist()
    
    # Removendo duplicatas e ordenando para evitar rótulos repetidos no eixo Y2
    unique_ticks_map = dict(zip(tick_values, tick_text_formatted))
    unique_tick_values = sorted(unique_ticks_map.keys())
    unique_tick_text = [unique_ticks_map[val] for val in unique_tick_values]
    if 0.0 not in unique_tick_values:
        unique_tick_values.insert(0, 0.0) # Insere o valor decimal zero
        unique_tick_text.insert(0, '00:00') # Insere o rótulo formatado zero

    fig2.update_layout(
        title=dict(
            text=f'Tarefas Reabertas vs. Tempo Médio (Distribuído por Equipes) <br>' 
                 f'<span style="font-size:16px;">(Top {top_n} de Tarefas Reabertas  )</span>',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#0A4D8C', family="Calibri")
        ),
        # Eixo X (Equipes)
        xaxis=dict(
            title='Equipe',
            tickangle=-45, 
            automargin=True,
            showgrid=True
        ),
        # Eixo Y Primário (Barras - Tarefas Reabertas)
        yaxis=dict(
            title='Número de Tarefas Reabertas',
            showgrid=False 
        ),
        # Eixo Y Secundário (Linha - Tempo Médio)
        yaxis2=dict(
            title='Tempo Médio de Esforço (hh:mm)', 
            overlaying='y',
            side='right', 
            showgrid=True,
            rangemode='tozero',
            tickfont=dict(color='#FC766A'),
            tickvals=unique_tick_values, 
            ticktext=unique_tick_text,
            # Se a lista de equipes for longa, talvez queira forçar a exibição de menos rótulos
            dtick=df_analise['media_esforco'].std() / 2 if df_analise['media_esforco'].std() > 0 else None 
        ),
        # Ajustes de legenda
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.0, 
            xanchor="right",
            x=1.0
        ),
        template='plotly_white',
        height=700 
    )
    
    st.plotly_chart(fig2, use_container_width=True)

    # Apresentação dos dados em lista
    st.markdown("### Tarefas por Time Responsável")

    time = st.selectbox("Filtrar por Time Responsável:", ["(Todos)"] + sorted(
        df_reabertas_sim['equipe_resp']
        .fillna("")
        .astype(str)
        .unique()
        ))


    df_view = df_reabertas_sim if time == "(Todos)" else df_reabertas_sim[df_reabertas_sim['equipe_resp'] == time]

    df_view['esforco_registrado'] = df_view['esforco_registrado'].apply(decimal_para_hora_min)

    coluna_formatada = {
    'tipo_tarefa': st.column_config.TextColumn("Tarefa"),
    'equipe_resp': st.column_config.TextColumn("Equipe Responsável"),
    'para': st.column_config.TextColumn("Responsável"),
    'dt_fechada': st.column_config.DateColumn("Fechada em:", format='DD/MM/YYYY'),
    'esforco_registrado': st.column_config.TextColumn("Esforço (hh:mm)")
    }

    st.dataframe(
        df_view[
            ["tipo_tarefa", "equipe_resp", "para", "dt_fechada", "esforco_registrado"]
        ].sort_values("equipe_resp", ascending=False),column_config=coluna_formatada,
        use_container_width=True,
        hide_index=True
    )

# ===================================================================
# 📊 Grafico 2 - Tempo entre entrega desejada x entrega fechada
# ===================================================================
if selecoes.get("SLA"):

    st.subheader(":blue[📈 Análise SLA]")
    multi = '''Foram consideradas somente tarefas encerradas com a data de entrega desejada preenchida.
               Utilize os filtros à esquerda para refinar sua análise.'''
    st.markdown(multi)

    #-----
    # GERAÇÃO DO GRÁFICO (Esforço Estimado vs. Esforço Registrado) - Agrupado por Tipo de Tarefa

    # Agrupar os dados por 'tipo_tarefa' para somar o esforço
    df_esforco_tipo = round(df_filtrado.groupby('tipo_tarefa').agg(
        esforco_estimado_medio=('esforco_estimado', 'mean'),
        esforco_registrado_medio=('esforco_registrado', 'mean')
    ).reset_index(),2)

    df_esforco_tipo['esforco_estimado_medio_format'] = df_esforco_tipo['esforco_estimado_medio'].apply(decimal_para_hora_min)
    df_esforco_tipo['esforco_registrado_medio_format'] = df_esforco_tipo['esforco_registrado_medio'].apply(decimal_para_hora_min)

    # Ordena para melhor visualização (por média estimada decrescente) e filtra o nr de retorno top n
    df_esforco_tipo = df_esforco_tipo.sort_values(by=['esforco_estimado_medio'], ascending=False).head(top_n)  

    # Determinar o valor máximo para a escala uniforme
    max_valor_horas = df_esforco_tipo[['esforco_estimado_medio', 'esforco_registrado_medio']].max().max()
    # Adicionamos uma pequena margem (ex: 5%) para que a barra mais alta não toque o topo do gráfico
    limite_superior = max_valor_horas * 1.05 
    y_range = [0, limite_superior] # Define a escala de 0 até o limite_superior

    fig1 = go.Figure()

    # Esforço Estimado - Eixo Y Primário
    fig1.add_trace(
        go.Bar(
            x=df_esforco_tipo['tipo_tarefa'], 
            y=df_esforco_tipo['esforco_estimado_medio'],
            name='Esforço Estimado (Horas)',
            marker_color='darkblue',
            text=df_esforco_tipo['esforco_estimado_medio_format'],  # Texto a ser exibido
            textposition='outside',  # Posição: acima das barras
            textfont=dict(size=12, color='#0A4D8C'),  # Formatação do texto        
            hovertemplate="Tarefa: %{x}<br>Esforço estimado médio: %{y}<extra></extra>"
        )
    )

    # Linha  - Esforço Registrado - Eixo Y Secundário
    fig1.add_trace(
        go.Scatter(
            x=df_esforco_tipo['tipo_tarefa'], 
            y=df_esforco_tipo['esforco_registrado_medio'],
            name='Esforço Registrado (Horas)',
            mode='lines+markers+text',
            marker=dict(size=8, symbol='circle'),
            line=dict(color='#FC766A', width=3),
            yaxis='y2', # Atribui ao eixo Y secundário
            text=df_esforco_tipo['esforco_registrado_medio_format'],  #Texto formatado (hh:mm)
            textposition='top center', 
            textfont=dict(size=11, color='#FC766A'),  # Formatação do texto
            customdata=df_esforco_tipo['esforco_registrado_medio_format'], 
            hovertemplate="Tarefa: %{x}<br>Esforço Médio Registrado: %{customdata}<extra></extra>"             
        )
    )

    fig1.update_layout(
        title=dict(
            text=f'Esforço Estimado vs. Esforço Registrado por Tipo de Tarefa <br>' 
                 f'<span style="font-size:16px;">(Top {top_n} de Esforço Estimado  )<br></span>',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#0A4D8C', family="Calibri")
        ),
        # Eixo X (Tipo de Tarefa)
        xaxis=dict(
            title='Tipo de Tarefa',
            tickangle=-45, 
            automargin=True,
            showgrid=True
        ),
        # Configuração do Eixo Y Primário (para as Barras - Média do tempo estimado)
        yaxis=dict(
            title='Esforço Estimado (hh:mm)',
            showgrid=True,
            range=y_range
        ),
        
        # Configuração do Eixo Y Secundário (para a Linha - Média do tempo registrada)
        yaxis2=dict(
            title='Esforço Registrado (hh:mm)',
            overlaying='y',  # Coloca este eixo sobre o primário
            side='right',    # Move o eixo para o lado direito
            showgrid=True,
            range=y_range
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.2
        ),
        barmode='group',
        template='plotly_white',
        height=600 
    )

    st.plotly_chart(fig1, use_container_width=True)    

    #-----
    # GERAÇÃO DO GRÁFICO (Tempo médio entre a data de entrega desejada e data de entrega fechada) - Agrupado por Tipo de Tarefa

    # Desconsiderar linhas onde dt_entrega_desejada estiver vazia
    df_sla = df_filtrado[df_filtrado['dt_entrega_desejada'].notna()]

    df_sla['dt_entrega_desejada'] = pd.to_datetime(df_sla['dt_entrega_desejada'], errors='coerce')
    df_sla['dt_fechada'] = pd.to_datetime(df_sla['dt_fechada'], errors='coerce')

    df_sla['diferenca_horas'] = df_sla['dt_fechada'] - df_sla['dt_entrega_desejada']
    
    df_sla['diferenca_horas'] = df_sla['diferenca_horas'].dt.total_seconds() / 3600    

    # Desconsiderar outliers
    # Calcula o primeiro quartil (Q1) e o terceiro quartil (Q3) da 'diferenca_horas'
    Q1 = df_sla['diferenca_horas'].quantile(0.25)
    Q3 = df_sla['diferenca_horas'].quantile(0.75)

    # Calcula o Intervalo Interquartil (IQR)
    IQR = Q3 - Q1

    # Define os limites para identificar outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filtra o DataFrame para remover os outliers
    df_sla_sem_outliers = df_sla[(df_sla['diferenca_horas'] >= lower_bound) & (df_sla['diferenca_horas'] <= upper_bound)]

    # Calcula a média da diferença de horas por tipo de tarefa usando os dados sem outliers
    df_sla_por_tarefa_sem_outliers = round(df_sla_sem_outliers.groupby('tipo_tarefa')['diferenca_horas'].mean().reset_index(),2)

    # Ordena os tipos de tarefa pelo tempo médio de SLA para melhor visualização
    df_sla_por_tarefa_sem_outliers = df_sla_por_tarefa_sem_outliers.sort_values('diferenca_horas', ascending=True)

    # Cria o gráfico de barras horizontal
    fig2 = px.bar(df_sla_por_tarefa_sem_outliers,
                x='diferenca_horas',
                y='tipo_tarefa',
                orientation='h',
                color='diferenca_horas', # Colore com base na diferença de horas
                color_continuous_scale='RdYlGn', # Escala de cores Vermelho-Amarelo-Verde
                labels={'diferenca_horas': 'Média da Diferença de Horas (SLA)', 'tipo_tarefa': 'Tipo de Tarefa'},
                title='Tempo Médio em horas (SLA) entre a Data Entrega Desejada e a Data Fechada por Tipo de Tarefa (Sem Outliers)',
                height=900) 

    # Ajusta o layout para melhor legibilidade
    fig2.update_layout(
        title_font_size=20,
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        xaxis_tickfont_size=10,
        yaxis_tickfont_size=10,
        yaxis_categoryorder='total ascending' # Garante a ordem das barras
    )

    st.plotly_chart(fig2, use_container_width=True)

    #-----
    # Apresentaçao dos dados que não foram apresentados no gráfico

    # Apresentação dos dados em lista
    st.markdown("### Tarefas que não foram consideradas no gráfico acima")
    st.markdown('##### Ocorrências sem data de entrega e Diferença(h) fora da média do intervalo 25% a 75%')

    # Filtra o DataFrame (df_filtered) para encontrar linhas onde 'diferenca_horas' é um outlier
    df_outliers_dif = df_sla[(df_sla['diferenca_horas'] < lower_bound) | (df_sla['diferenca_horas'] > upper_bound)]

    # Filtra o DataFrame original (df) para encontrar linhas onde 'dt_entrega_desejada' é nula
    df_outliers_estimada_nula = df_filtrado[df_filtrado['dt_entrega_desejada'].isna()]

    # Combina os dois conjuntos de outliers e remove duplicatas (caso uma linha se enquadre em ambas as categorias)
    df_outliers = pd.concat([df_outliers_dif, df_outliers_estimada_nula]).drop_duplicates()

    # Total de ocorrências excluídas
    total_ocorrencias = df_outliers['cliente'].count()

    # Validação: caso não existam dados filtrados
    if total_ocorrencias == 0:
        st.warning("⚠️ Não existem ocorrências desconsideradas.")
        st.stop()

    # Calcula o SLA destas tarefas
    # Converter ambas as colunas para datetime
    df_outliers['dt_fechada'] = pd.to_datetime(df_outliers['dt_fechada'], errors='coerce')
    df_sla['dt_entrega_desejada'] = pd.to_datetime(df_sla['dt_entrega_desejada'], errors='coerce')

    # Calcular diferença em horas
    df_outliers['diferenca_horas'] = (df_outliers['dt_fechada'] - df_sla['dt_entrega_desejada']).dt.total_seconds() / 3600

    coluna_formatada = {
    'cliente': st.column_config.TextColumn("Cliente"),
    'tipo_tarefa': st.column_config.TextColumn("Tarefa"),
    'equipe': st.column_config.TextColumn("Equipe Responsável"),
    'para': st.column_config.TextColumn("Responsável"),
    'dt_entrega_desejada': st.column_config.DateColumn("Data Entrega Desejada", format='DD/MM/YYYY'),
    'dt_fechada': st.column_config.DateColumn("Data Fechada", format='DD/MM/YYYY'),
    'diferenca_horas': st.column_config.NumberColumn("Diferença(h)", format='%.2f')
    }

    st.dataframe(
        df_outliers[
            ["cliente", "tipo_tarefa", "equipe", "para", "dt_entrega_desejada", "dt_fechada", "diferenca_horas"]
        ].sort_values("dt_entrega_desejada", ascending=False),column_config=coluna_formatada,
        use_container_width=True,
        hide_index=True
    ) 

# ===================================================================
# 📊 Grafico 3 - Média de horas para fechamento por tipo de tarefa
# ===================================================================

if selecoes.get("Tempo médio por Tarefas"):

    st.subheader(":blue[📈 Média de horas para fechamento por tipo de tarefa]")
    multi = '''Foram consideradas somente tarefas encerradas.
               Utilize os filtros à esquerda para refinar sua análise.'''
    st.markdown(multi)

    # Considerar linhas onde dt_fechada estiver preenchida
    df_tmd = df_filtrado[df_filtrado['dt_fechada'].notna()]

    # Total de tarefas por tipo
    total_tarefas = df_tmd.groupby('tipo_tarefa').size().reset_index(name='Total_Tarefas')

    # Média de horas por tipo
    media_horas = df_tmd.groupby('tipo_tarefa')['esforco_registrado'].mean().reset_index()
    media_horas = media_horas.round(2)
    media_horas['media_formatada'] = media_horas['esforco_registrado'].apply(decimal_para_hora_min)

    # Combinar as métricas em um único DataFrame
    df_grafico = pd.merge(total_tarefas, media_horas, on='tipo_tarefa')

    # --- Selecionar top n pelo total de tarefas ---
    df_grafico = df_grafico.sort_values(by='Total_Tarefas', ascending=False).head(top_n)

    # --- Criar gráfico combinado ---
    fig1 = go.Figure()

    # Barras: total de tarefas
    fig1.add_trace(go.Bar(
        x=df_grafico['tipo_tarefa'],
        y=df_grafico['Total_Tarefas'],
        name='Total de Tarefas',
        text=df_grafico['Total_Tarefas'],
        textposition='outside',
        yaxis='y1'
    ))

    # Linha: média de horas
    fig1.add_trace(go.Scatter(
        x=df_grafico['tipo_tarefa'],
        y=df_grafico['esforco_registrado'],
        name='Média de Horas',
        mode='lines+markers+text',
        text=df_grafico['media_formatada'],
        textfont=dict(color='black'),
        textposition='bottom center',
        marker=dict(color='orange', size=10),
        yaxis='y2'
    ))

    # --- Layout ---
    fig1.update_layout(
        title=dict(
            text=f'Total de Tarefas e SLA Médio de Encerramento (Esforço registrado) <br>' 
                f'<span style="font-size:16px;">(Somente os {top_n} tipos de tarefa mais executadas)</span>',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#0A4D8C', family="Calibri")
        ),
        xaxis_title='Tipo de Tarefa',
        yaxis=dict(
            title='Total de Tarefas',
            showgrid=False,
            zeroline=False
        ),
        yaxis2=dict(
            title='Média de Horas',
            overlaying='y',
            side='right',
            showgrid=False,
            zeroline=False
        ),
        legend=dict(x=0.9, y=1.0),
        barmode='group',
        template='plotly_white',
        height=600
    )

    st.plotly_chart(
        fig1,
        config={"responsive": True},  # substitui use_container_width
    )

    # Apresentação dos dados em lista
    st.markdown("### Detalhamento Tarefas")

    df_summary = df_filtrado.groupby('tipo_tarefa', as_index=False).agg(
        total_tarefa=('id_tarefa', 'count'),
        media_esforco=('esforco_registrado','mean')).reset_index()

    df_summary['media_formatada'] = df_summary['media_esforco'].apply(decimal_para_hora_min)

    df_detalhe = df_filtrado.copy()
    df_detalhe['esforco_formatado'] = df_detalhe['esforco_registrado'].apply(decimal_para_hora_min)

    colunas_para_exibir = [
        "cliente", 
        "para", 
        "id_tarefa", 
        "esforco_formatado"
    ]

    config_colunas = {
        "cliente": st.column_config.TextColumn("Cliente"),
        "para": st.column_config.TextColumn("Responsável"),
        "id_tarefa": st.column_config.TextColumn("Nr Tarefa"),
        "esforco_formatado": st.column_config.TextColumn("Esforço Registrado (hh:mm)")
    }

    for _, row in df_summary.iterrows():
        df_detalhe_filtrado = df_detalhe[df_detalhe["tipo_tarefa"] == row["tipo_tarefa"]]
        with st.expander(f"**{row['tipo_tarefa']}** | Quantidade Tarefas: {row['total_tarefa']} | Esforço Médio: {row['media_formatada']}"):
             st.dataframe(
                 df_detalhe_filtrado[colunas_para_exibir],  
                 column_config=config_colunas,     
                 use_container_width=True,
                 hide_index=True
             )


# ===================================================================
# 📊 Grafico 4 - Média de horas para fechamento por cliente
# ===================================================================

if selecoes.get("Tempo médio por Clientes"):

    st.subheader(":blue[📈 Média de horas para fechamento por cliente]")
    multi = '''Foram consideradas somente tarefas encerradas.
               Utilize os filtros à esquerda para refinar sua análise.'''
    st.markdown(multi)

    # Filtra para linhas onde 'dt_fechada' está preenchida
    df_clientes = df_filtrado[df_filtrado['dt_fechada'].notna()]

    # Total de tarefas por cliente
    total_tarefas_cliente = df_clientes.groupby('cliente').size().reset_index(name='Total_Tarefas')

    # Média de esforço registrado por cliente
    media_horas_cliente = df_clientes.groupby('cliente')['esforco_registrado'].mean().reset_index()
    media_horas_cliente = media_horas_cliente.round(2)
    media_horas_cliente['media_formatada'] = media_horas_cliente['esforco_registrado'].apply(decimal_para_hora_min)

    # Combina as duas métricas
    df_grafico_cliente = pd.merge(total_tarefas_cliente, media_horas_cliente, on='cliente')

    # Ordenar e selecionar top N clientes conforme top_n do sidebar
    df_grafico_cliente = df_grafico_cliente.sort_values(by='Total_Tarefas', ascending=False).head(top_n)

    # Criar gráfico combinado
    fig_cliente = go.Figure()

    # Barras para total de tarefas
    fig_cliente.add_trace(go.Bar(
        x=df_grafico_cliente['cliente'],
        y=df_grafico_cliente['Total_Tarefas'],
        name='Total de Tarefas',
        text=df_grafico_cliente['Total_Tarefas'],
        textposition='outside',
        yaxis='y1'
    ))

    # Linha para média de horas
    fig_cliente.add_trace(go.Scatter(
        x=df_grafico_cliente['cliente'],
        y=df_grafico_cliente['esforco_registrado'],
        name='Média de Horas',
        mode='lines+markers+text',
        text=df_grafico_cliente['media_formatada'],
        textfont=dict(color='black'),
        textposition='bottom center',
        marker=dict(color='orange', size=10),
        yaxis='y2'
    ))

    # Configurações do layout do gráfico
    fig_cliente.update_layout(
        title=dict(
            text=f'Total de Tarefas e SLA Médio de Encerramento (Esforço registrado) <br>'
                 f'<span style="font-size:16px;">(Somente os {top_n} clientes com maior número de tarefas solicitadas)</span>',
            x=0.5,
            xanchor='center',
            font=dict(size=20, color='#0A4D8C', family="Calibri")
        ),
        xaxis_title='Cliente',
        yaxis=dict(
            title='Total de Tarefas',
            showgrid=False,
            zeroline=False,
        ),
        yaxis2=dict(
            title='Média de Horas',
            overlaying='y',
            side='right',
            showgrid=False,
            zeroline=False
        ),
        legend=dict(x=0.9, y=1.0),
        barmode='group',
        template='plotly_white',
        height=700
    )

    st.plotly_chart(fig_cliente, config={"responsive": True})

    # Apresentação dos dados em lista
    st.markdown("### Detalhamento Tarefas x Clientes")

    df_summary = df_filtrado.groupby('cliente', as_index=False).agg(
        total_tarefa=('id_tarefa', 'count'),
        media_esforco=('esforco_registrado','mean')).reset_index()

    df_summary['media_formatada'] = df_summary['media_esforco'].apply(decimal_para_hora_min)

    df_detalhe = df_filtrado.copy()
    df_detalhe['esforco_formatado'] = df_detalhe['esforco_registrado'].apply(decimal_para_hora_min)
    
    colunas_para_exibir = [
        "tipo_tarefa", 
        "equipe",
        "para", 
        "id_tarefa", 
        "esforco_formatado"
    ]

    config_colunas = {
        "tipo_tarefa": st.column_config.TextColumn("Tarefa"),
        'equipe': st.column_config.TextColumn("Equipe Responsável"),
        "para": st.column_config.TextColumn("Responsável"),
        "id_tarefa": st.column_config.TextColumn("Nr Tarefa"),
        "esforco_formatado": st.column_config.TextColumn("Esforço Registrado (hh:mm)")
    }

    for _, row in df_summary.iterrows():
        df_detalhe_filtrado = df_detalhe[df_detalhe["cliente"] == row["cliente"]]
        with st.expander(f"**{row['cliente']}** | Quantidade Tarefas: {row['total_tarefa']} | Esforço Médio: {row['media_formatada']}"):
             st.dataframe(
                 df_detalhe_filtrado[colunas_para_exibir],  
                 column_config=config_colunas,     
                 use_container_width=True,
                 hide_index=True
             )
