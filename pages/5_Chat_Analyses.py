import pandas as pd
import random
import streamlit as st

################################################################
# Configurações da página

# Seta configurações da página
st.set_page_config(
    page_title="Projeto Analise Eleitoral",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="auto",
)

################################################################
# Carregamento de dados

def load_data():
    df = pd.read_csv('./datas/votacao_secao_2020_PARAUAPEBAS_PA.csv',
                    dtype={"SG_UE": "string"}, 
                    sep=',' )

    df["NR_NM_VOTAVEL"] = df["NR_VOTAVEL"].map(str) + " - " + df["NM_VOTAVEL"]

    return df

df = load_data()

################################################################
# Sessão de Gráficos

st.write("# Sessão de gráficos")

st.divider()

################################################################
# Quantidade de Votos por local de votação

st.write("## Quantidade de Votos por local de votação")

NM_LOCAL_VOTACAO_LIST = []
NR_NM_VOTAVEL_LIST = []

col1, col2 = st.columns(2)

with col1:
    NR_NM_VOTAVEL_LIST = st.sidebar.multiselect('Selecione os candidatos:', list(df["NR_NM_VOTAVEL"].unique()))

with col2:
    NM_LOCAL_VOTACAO_LIST  = st.sidebar.multiselect('Selecione os locais de votação:', list(df["NM_LOCAL_VOTACAO"].unique()))

df = df.loc[ 
            (df["NM_LOCAL_VOTACAO"].isin(NM_LOCAL_VOTACAO_LIST)) &
            (df["NR_NM_VOTAVEL"].isin(NR_NM_VOTAVEL_LIST)), 
            ["NM_LOCAL_VOTACAO","NR_NM_VOTAVEL","QT_VOTOS"] 
        ]

df = df.groupby(["NM_LOCAL_VOTACAO","NR_NM_VOTAVEL"])

df = df["QT_VOTOS"].sum().reset_index(name='QT_VOTOS')

df["NM_LOCAL_VOTACAO-NR_NM_VOTAVEL"] = df["NR_NM_VOTAVEL"].map(str) + " - " + df["NM_LOCAL_VOTACAO"]

df["colors"] = df["NM_LOCAL_VOTACAO-NR_NM_VOTAVEL"] + " - " + ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]

df = df.sort_values(by=["QT_VOTOS", "NR_NM_VOTAVEL"], ascending=False).reset_index(drop=True)

x = "NM_LOCAL_VOTACAO-NR_NM_VOTAVEL"
y = "QT_VOTOS"
colors = "colors"

st.bar_chart(data=df, x=x, y=y, color=colors)

with st.expander("Dados e Explicação:"):
    st.write("""
        O gráfico é gerador a partir do agrupamento das colunas 
        NM_LOCAL_VOTACAO e NR_NM_VOTAVEL, e aplicado o metodo de 
        agregação com soma a coluna QT_VOTOS
    """)
    st.dataframe(df)


