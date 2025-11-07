
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

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

st.set_page_config(page_title="Dados Informática Ltda", layout="wide")

#CSV
df=pd.read_csv('/Users/margarida/Documents/Curso Python/Educ360/repo/Educ360/Python - Semana 7/vendas.csv',
               parse_dates=['data_venda'])


# --- Barra Lateral (Filtros) ---
st.sidebar.header("🔍 Filtros para Análise")

# Calcular percentual de desconto
df['valor_sem_desconto'] = df['quantidade'] * df['preco_unitario']
df['percentual_desconto'] = (df['desconto'] / df['valor_sem_desconto']).fillna(0) * 100 


#Combo das datas
# recebe todas as datas (df), classifica e filtra somente 1 de cada (unique)
datas_unicas = sorted(df['data_venda'].dt.strftime("%d-%m-%Y").unique())
#usando os recursos do st, crio uma barra lateral com as opções (selectbox) com a primeira opçao como Todas
opcao_data = st.sidebar.selectbox("Selecione a data:",options=["Todas"] + datas_unicas)

#Combo de categorias

categorias = sorted(df['categoria'].unique())
opcao_categoria = st.sidebar.selectbox("Selecione uma categoria:", options=["Todas"] + categorias)

#Combo de descontos

min_desc = float(df['percentual_desconto'].min())
max_desc = float(df['percentual_desconto'].max())
filtro_desconto = st.sidebar.slider('Faixa de Desconto (%)',
                                    min_value=min_desc,
                                    max_value=max_desc,
                                    value=(min_desc, max_desc))

min_desconto = round(filtro_desconto[0],2)
max_desconto = round(filtro_desconto[1],2)
                  
#Aplicar filtros

df_filtrado = df.copy()

if opcao_data != "Todas":
    df_filtrado = df_filtrado[df_filtrado["data_venda"].dt.strftime("%d-%m-%Y") == opcao_data]

if opcao_categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria"] == opcao_categoria]

df_filtrado = df_filtrado[
    (df_filtrado['percentual_desconto'] >= filtro_desconto[0]) &
    (df_filtrado['percentual_desconto'] <= filtro_desconto[1])
]
    
# Cálculos para os cards
total_vendas = df_filtrado['quantidade'].sum()
total_vl_vendas = df_filtrado['valor_total'].sum() if 'valor_total' in df_filtrado.columns else 0.
total_vl_vendas = formata_brasileiro(total_vl_vendas)
fat_cat = df.groupby('categoria')['valor_total'].mean()
fat_cat = formata_brasileiro(fat_cat.iloc[0])

# Verificar se não há dados
if total_vendas == 0:
    st.warning("⚠️ Não existem dados que atendam aos filtros selecionados.")
    st.stop()

st.title(":blue[🎲 Dados Informática Ltda]")
    
# Exibir os cards lado a lado
card1, card2, card3 = st.columns(3)
with card1:
    card_com_borda("Nr Vendas", total_vendas)
with card2:
    card_com_borda("Faturamento Total Período", f"R$ {total_vl_vendas}")
with card3:
    card_com_borda("Faturamento Medio", f"R$ {fat_cat}")

st.markdown("---")  

# Composição dos gráficos

st.subheader(":blue[📈 Análise Faturamento]")
multi = '''Explore as informações das vendas do último período. Utilize os filtros à esquerda para refinar sua análise.'''
st.markdown(multi)
l1_col1, l1_col2 = st.columns(2)
l2_col1, l2_col2 = st.columns(2)

# Grafico 1 - Total de Faturamento por Categoria

fat_categorias = df_filtrado.groupby("categoria").agg({"valor_total": 'sum'}).reset_index()

fig1 = px.bar(
    fat_categorias,
    x = "categoria",
    y = "valor_total",
    color="categoria",
    title=f"Total de Faturamento por Categoria<br>({opcao_categoria})",
    text="valor_total",
    color_discrete_sequence = px.colors.qualitative.Pastel
)

fig1.update_layout(xaxis_title="Categoria(s)", yaxis_title="Total de Faturamento")
fig1.update_layout(title_x=0.5, title_xanchor='center')
l1_col1.plotly_chart(fig1, use_container_width=True)

# Grafico 2 - Evolução de Faturamento por data

# Para o gráfico 2, aplicar filtro apenas na categoria, sem considerar o filtro de data
if opcao_categoria != "Todas":
    df_filtrado2 = df[df["categoria"] == opcao_categoria]
else:
    df_filtrado2 = df    

fat_data = df_filtrado2.groupby('data_venda')['valor_total'].sum().reset_index()

fig2 = px.line(
    fat_data, 
    x='data_venda', 
    y='valor_total', 
    title=f'Evolução do Faturamento por Data<br>Categoria: {opcao_categoria}',
    color_discrete_sequence = px.colors.qualitative.Pastel
    )

fig2.update_layout(xaxis_title='Data da Venda', yaxis_title='Faturamento Total (R$)')
fig2.update_layout(title_x=0.5, title_xanchor='center')
l1_col2.plotly_chart(fig2, use_container_width=True)

# Grafico 3 - Desconto Médio por Categoria

desc_cat = df_filtrado.groupby('categoria').agg({'percentual_desconto':'mean', 'quantidade':'sum'}).reset_index()

fig3 = px.pie(
    desc_cat, 
    names='categoria', 
    values='quantidade',
    color="categoria",
    title=f'Desconto Médio por Categoria<br>Faixa de {min_desconto}% até {max_desconto}% <br> {opcao_categoria}',
    color_discrete_sequence = px.colors.qualitative.Pastel,
    hole=0.3,
    custom_data=['percentual_desconto']
    )

# Mostrar na fatia a média do desconto formatada
fig3.update_traces(
    texttemplate='%{customdata[0]:.2f} %',
    textposition='inside',
    hovertemplate='%{label}<br>Quantidade: %{value}<br>Desconto médio: %{customdata[0]:.2f}%<extra></extra>'
)
fig3.update_layout(title_x=0.5, title_xanchor='center')
l2_col1.plotly_chart(fig3, use_container_width=True)

# Grafico 4

# Agrupar os dados por categoria resumindo vendas e desconto
desc_cat = df_filtrado.groupby('categoria').agg({
    'valor_total': 'sum',
    'percentual_desconto': 'mean'
}).reset_index()

fig4 = go.Figure()

# Adicionar barras para o número de vendas
fig4.add_trace(go.Bar(
    x=desc_cat['categoria'],
    y=desc_cat['valor_total'],
    name='Valor Total de Vendas',
    yaxis='y1',
    marker_color='blue',
    text=desc_cat['valor_total'].round(2),
    textposition='auto'
))

# Adicionar linha para percentual de desconto
fig4.add_trace(go.Scatter(
    x=desc_cat['categoria'],
    y=desc_cat['percentual_desconto'],
    name='Percentual de Desconto',
    yaxis='y2',
    mode='lines+markers',
    line=dict(color='red', width=3),
    marker=dict(size=8),
    text=desc_cat['percentual_desconto'].round(2),
    textposition='top center'
))

# Configurar layout com dois eixos y
fig4.update_layout(
    title='Valor Total de Vendas e Percentual de Desconto por Categoria',
    xaxis=dict(title='Categoria'),
    yaxis=dict(
        title='Valor Total de Vendas',
        showgrid=False
    ),
    yaxis2=dict(
        title='Percentual de Desconto (%)',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(x=0.1, y=1.1, orientation='h'),
    margin=dict(t=80),
    template="plotly_white"
)

fig4.update_layout(title_x=0.5, title_xanchor='center')
l2_col2.plotly_chart(fig4, use_container_width=True)

# Visão das vendas

st.subheader(f":blue[💰 Vendas Data: {opcao_data} - Categoria: {opcao_categoria} - Faixa Desconto de {min_desconto}% até {max_desconto}%]")

# Formatar o valor para apresentar virgula no lugar do ponto
df_filtrado['preco_unitario_form'] = df_filtrado['preco_unitario'].apply(formata_brasileiro) 
df_filtrado = df_filtrado.drop('preco_unitario', axis=1)
df_filtrado['valor_formatado'] = df_filtrado['valor_total'].apply(formata_brasileiro) 
df_filtrado['desconto_form'] = df_filtrado['desconto'].apply(formata_brasileiro) 
df_filtrado['perc_desconto'] = df_filtrado['percentual_desconto'].apply(formata_brasileiro)
# Excluir colunas na apresentação
df_filtrado = df_filtrado.drop('valor_total', axis=1)
df_filtrado = df_filtrado.drop('valor_sem_desconto', axis=1)
df_filtrado = df_filtrado.drop('percentual_desconto', axis=1)
df_filtrado = df_filtrado.drop('desconto', axis=1)


coluna_formatada = {
    'data_venda': st.column_config.DateColumn("Data Venda", format='DD/MM/YYYY'),
    'quantidade': st.column_config.TextColumn("Quantidade"),
    'desconto_form': st.column_config.TextColumn("Desconto"),
    'perc_desconto': st.column_config.TextColumn("Desconto(%)"),
    'nome_produto': st.column_config.TextColumn("Produto"),
    'categoria': st.column_config.TextColumn("Categoria"),
    'preco_unitario_form': st.column_config.TextColumn("Unid.(R$)"),
    'valor_formatado': st.column_config.TextColumn("Valor Venda(R$)")
}
st.dataframe(df_filtrado, column_config=coluna_formatada, use_container_width= True)


