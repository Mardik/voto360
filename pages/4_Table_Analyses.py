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

# cidade = 'PARAUAPEBAS'

# df = df.loc[:, ["SG_UF",
#                 "SG_UE", 
#                 "NM_UE", 
#                 "CD_MUNICIPIO", 
#                 "NM_MUNICIPIO", 
#                 "NR_ZONA", 
#                 "NR_SECAO", 
#                 "DS_CARGO", 
#                 "NR_VOTAVEL",
#                 "NM_VOTAVEL",
#                 "QT_VOTOS", 
#                 "NR_LOCAL_VOTACAO", 
#                 "NM_LOCAL_VOTACAO", 
#                 "DS_LOCAL_VOTACAO_ENDERECO"]]


# df = df[df["NM_UE"] == cidade]

################################################################
# Sessão de Formulários e Filtros

# Criar um dicionário para armazenar os valores selecionados
valores = {}

# Iterar sobre as colunas do DataFrame
for coluna in df.columns:
    # Criar um formulário de múltiplas opções
    valores[coluna] = st.sidebar.multiselect(coluna, list(df[coluna].unique()))

# Criar um filtro a partir do dicionário
filtro = []
for coluna, valores_selecionados in valores.items():
    if valores_selecionados:
        filtro.append(f"({coluna} in {valores_selecionados})")

query = ' and '.join(filtro)

################################################################
# Sessão de Dataframe

st.write("# Sessão de Dataframe")

# Definie as configurações de exibição dos dados nas colunas
column_config={
        "CD_MUNICIPIO": st.column_config.NumberColumn(
            "CD_MUNICIPIO",
            help="Código TSE do município onde ocorreu a eleição",
            format="%d",
        ),
        "NR_VOTAVEL": st.column_config.NumberColumn(
            "NR_VOTAVEL",
            help="""
## Número do votável. Pode assumir os valores:

    - número da candidata ou candidato, quando voto nominal;
    - número do partido, quando voto em legenda;
    - número 95, quando voto em branco;
    - número 96, quando voto nulo;
    - número 97, quando voto anulado e apurado em separado.

            """,
            format="%d",
        ),        
        "NR_LOCAL_VOTACAO": st.column_config.NumberColumn(
            "NR_LOCAL_VOTACAO",
            help="Número do local de votação da eleitora ou eleitor.",
            format="%d",
        ),      
    }

if query:
    # Aplicar o filtro ao DataFrame
    df_filtrado = df.query(query)

    # Exibir o DataFrame filtrado
    st.dataframe(df_filtrado, column_config=column_config)
else:
    # Exibir o DataFrame sem filtro
    st.dataframe(df, column_config=column_config)