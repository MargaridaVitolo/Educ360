import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
#               DADOS (EXEMPLO)
# ==========================================

df = pd.DataFrame({
    "Categoria": ["Eletrônicos", "Eletrônicos", "Eletrônicos",
                  "Roupas", "Roupas", "Roupas",
                  "Alimentos", "Alimentos"],
    "Produto": ["TV", "Notebook", "Smartphone",
                "Camiseta", "Calça", "Casaco",
                "Arroz", "Feijão"],
    "Vendas": [10000, 15000, 12000,
               3000, 5000, 4500,
               2000, 2500]
})

# ==========================================
#             INTERFACE STREAMLIT
# ==========================================

st.set_page_config(page_title="Drill-down com Streamlit", layout="wide")

st.title("📊 Exemplo de Drill-down com Streamlit")

# ============= NÍVEL 1 ==============
st.subheader("🔹 Visão Geral — Vendas por Categoria")

df_summary = df.groupby("Categoria", as_index=False).agg({"Vendas": "sum"})

st.dataframe(df_summary, use_container_width=True)

st.markdown("---")

# ============= NÍVEL 2 ==============
st.subheader("🔻 Drill-down — Detalhamento por Categoria")

categoria_selecionada = st.selectbox(
    "Selecione uma categoria para visualizar os detalhes:",
    options=df_summary["Categoria"]
)

df_detalhes = df[df["Categoria"] == categoria_selecionada]

st.write(f"### Produtos da categoria **{categoria_selecionada}**:")
st.dataframe(df_detalhes, use_container_width=True)

# ============= EXTRA: EXPANDERS ==============

st.markdown("---")
st.subheader("📂 Drill-down Alternativo por Expansão (Expander)")

for _, row in df_summary.iterrows():
    with st.expander(f"""{row['Categoria']}{row['Vendas']:>40}"""):
        st.dataframe(df[df["Categoria"] == row["Categoria"]], use_container_width=True)



