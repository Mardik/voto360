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

@st.cache_data 
def load_data():
    df = pd.read_csv('./datas/votacao_secao_2020_PARAUAPEBAS_PA.csv',
                    dtype={"SG_UE": "string"}, 
                    sep=',' )
    return df

df = load_data()
df_g = df

################################################################
# Sessão de Gráficos

st.write("# Sessão de gráficos")

################################################################
# Quantidade de Votos por local de votação

st.write("## Quantidade de Votos por local de votação")

NM_LOCAL_VOTACAO_LIST = []
NR_VOTAVEL_LIST = []

col1, col2 = st.columns(2)

with col1:
    NR_VOTAVEL_LIST = st.multiselect('Selecione os candidatos:', list(df["NR_VOTAVEL"].unique()))

with col2:
    NM_LOCAL_VOTACAO_LIST  = st.multiselect('Selecione os locais de votação:', list(df["NM_LOCAL_VOTACAO"].unique()))

df = df.loc[ 
            (df["NM_LOCAL_VOTACAO"].isin(NM_LOCAL_VOTACAO_LIST)) &
            (df["NR_VOTAVEL"].isin(NR_VOTAVEL_LIST)), 
            ["NM_LOCAL_VOTACAO","NR_VOTAVEL","QT_VOTOS"] 
        ]

df = df.groupby(["NM_LOCAL_VOTACAO","NR_VOTAVEL"])

df = df["QT_VOTOS"].sum().reset_index(name='QT_VOTOS')

df["NM_LOCAL_VOTACAO-NR_VOTAVEL"] = df["NR_VOTAVEL"].map(str) + " - " + df["NM_LOCAL_VOTACAO"]

df["colors"] = df["NM_LOCAL_VOTACAO-NR_VOTAVEL"] + " - " + ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]

df = df.sort_values(by=["QT_VOTOS", "NR_VOTAVEL"], ascending=False).reset_index(drop=True)

x = "NM_LOCAL_VOTACAO-NR_VOTAVEL"
y = "QT_VOTOS"
colors = "colors"

st.bar_chart(data=df, x=x, y=y, color=colors)

with st.expander("Dados e Explicação:"):
    st.write("""
        O gráfico é gerador a partir do agrupamento das colunas 
        NM_LOCAL_VOTACAO e NR_VOTAVEL, e aplicado o metodo de 
        agregação com soma a coluna QT_VOTOS
    """)
    st.dataframe(df)


################################################################
# Quantidade de Votos por local de votação com colunas dinâmicas

st.write("## Quantidade de Votos por local de votação com colunas dinâmicas")

colunas_x = []
colunas_y = []

col1, col2 = st.columns(2)

with col1:
    st.header("Eixo Y")
    colunas_x = st.multiselect('Selecione umas ou mais colunas a serem agrupadas:', df_g.columns)


with col2:
    st.header("Eixo X")
    colunas_y = st.selectbox('Selecione uma coluna:', df_g.columns, index=None)


st.write([*colunas_x,colunas_y])

colums = [*colunas_x,colunas_y]

if colunas_y:
    df_g = df_g[colums]

valores = {}

# Iterar sobre as colunas do DataFrame
for coluna in colunas_x:
    # Criar um formulário de múltiplas opções
    valores[coluna] = st.sidebar.multiselect(coluna, list(df_g[coluna].unique()))

# Criar um filtro a partir do dicionário
filtro = []
for coluna, valores_selecionados in valores.items():
    if valores_selecionados:
        filtro.append(f"({coluna} in {valores_selecionados})")

query = ' and '.join(filtro)

st.write(query)

df_filtrado = ''

if query:
    # Aplicar o filtro ao DataFrame
    df_filtrado = df_g.query(query)

    # Exibir o DataFrame filtrado
    st.dataframe(df_filtrado)
else:
    df_filtrado = df_g
    # Exibir o DataFrame sem filtro
    st.dataframe(df_filtrado)

################################################################
# Daqui para frente n está funcionando
# if len(colunas_x) > 1:
# df_filtrado = df_filtrado.groupby(colunas_x)
# df_filtrado = df_filtrado["QT_VOTOS"].sum().reset_index(name='QT_VOTOS')

# df_filtrado

# df["NM_LOCAL_VOTACAO-NR_VOTAVEL"] = df["NR_VOTAVEL"].map(str) + " - " + df["NM_LOCAL_VOTACAO"]

# df["colors"] = df["NM_LOCAL_VOTACAO-NR_VOTAVEL"] + " - " + ["#"+''.join([random.choice('ABCDEF0123456789') for i in range(6)])]

# df = df.sort_values(by=["QT_VOTOS", "NR_VOTAVEL"], ascending=False).reset_index(drop=True)

# df

# x = "NM_LOCAL_VOTACAO-NR_VOTAVEL"
# y = "QT_VOTOS"
# colors = "colors"

# st.bar_chart(data=df, x=x, y=y, color=colors)
