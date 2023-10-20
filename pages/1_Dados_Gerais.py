import pandas as pd
import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

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
    df["NR_NM_VOTAVEL"] = df["NR_VOTAVEL"].map(str) + " - " + df["NM_VOTAVEL"]

    return df

df = load_data()

# st.dataframe(df)

################################################################
# Apresentação da Página

st.write("# Perfil da Eleição")
st.write("""
        Objetivos: 
        - Levantar dados gerais de votação da eleição
        - Apresentar a perspectiva desses dados em formato tabular e gráficos;
        """)

st.divider()

################################################################
# Dados Gerais da Eleição

st.write("## Dados Gerais da Eleição")

df_tmp = df.loc[
            (df["CD_CARGO"] == 13) & 
            (df['NR_VOTAVEL'].astype(str).str.len() == 5), 'NR_VOTAVEL']

qnt_total_de_candidatos_cargo_verador = len(df_tmp.unique())

df_tmp = df.loc[(df["CD_CARGO"] == 11) & (~df['NR_VOTAVEL'].isin([95, 96, 97])), 'NR_VOTAVEL']

qnt_total_de_candidatos_cargo_prefeito = len(df_tmp.unique())

df_tmp = df[~df['NR_VOTAVEL'].isin([95, 96, 97])]

qnt_votos_validos = df_tmp['QT_VOTOS'].sum()

df_tmp = df[(df["CD_CARGO"] == 13) & ~df['NR_VOTAVEL'].isin([95, 96, 97])]

qnt_votos_validos_cargo_verador = df_tmp['QT_VOTOS'].sum()

df_tmp = df[(df["CD_CARGO"] == 11) & (~df['NR_VOTAVEL'].isin([95, 96, 97]))]

qnt_votos_validos_cargo_prefeito = df_tmp['QT_VOTOS'].sum()

df_tmp = df[df['NR_VOTAVEL'] == 95]

qnt_de_votos_em_branco = df_tmp['QT_VOTOS'].sum()

df_tmp = df[df['NR_VOTAVEL'] == 96]

qnt_de_votos_nulo = df_tmp['QT_VOTOS'].sum()

df_tmp = df[df['NR_VOTAVEL'] == 97]

qnt_de_votos_anulados = df_tmp['QT_VOTOS'].sum()

qnt_total_de_votos = qnt_votos_validos+qnt_de_votos_em_branco+qnt_de_votos_nulo

st.write(f'#### Quantidade total de candidatos a Vereador: {qnt_total_de_candidatos_cargo_verador}')
st.write(f'#### Quantidade total de candidatos a Prefeito: {qnt_total_de_candidatos_cargo_prefeito}')
st.write(f'#### Quantidade de votos validos para Vereador: {qnt_votos_validos_cargo_verador}')
st.write(f'#### Quantidade de votos validos para Prefeito: {qnt_votos_validos_cargo_prefeito}')
st.write(f'#### Quantidade total de votos validos para Prefeito e Vereador: {qnt_votos_validos}')
st.write(f'#### Quantidade de votos em branco: {qnt_de_votos_em_branco}')
st.write(f'#### Quantidade de votos nulos: {qnt_de_votos_nulo}')
st.write(f'#### Quantidade de votos anulados: {qnt_de_votos_anulados}')

################################################################
# Sessão de Dados Tabulares

st.write("## Sessão de Dados Tabulares")

st.divider()

st.write("#### Quantidade Total de Votos por candidado a Prefeito:")

df_tmp = df.loc[(df["CD_CARGO"] == 11) & (~df['NR_VOTAVEL'].isin([95, 96, 97])), ['NR_VOTAVEL','NR_NM_VOTAVEL','QT_VOTOS']]

df_tmp = df_tmp.groupby(['NR_VOTAVEL',"NR_NM_VOTAVEL"])

df_tmp = df_tmp["QT_VOTOS"].sum().reset_index(name='QT_VOTOS')

df_tmp = df_tmp.sort_values(by=["QT_VOTOS"], ascending=False).reset_index(drop=True)

df_tmp["QT_VOTOS_PERCENTUAL"] = (df_tmp["QT_VOTOS"] / qnt_votos_validos_cargo_prefeito) * 100

df_prefeito = df_tmp

st.dataframe(df_prefeito)

st.write("#### Quantidade Total de Votos dos 41 candidados a Vereador mais bem votados:")

df_tmp = df.loc[
            (df["CD_CARGO"] == 13) & 
            (df['NR_VOTAVEL'].astype(str).str.len() == 5), ['NR_VOTAVEL','NR_NM_VOTAVEL','QT_VOTOS']]

df_tmp = df_tmp.groupby(["NR_VOTAVEL","NR_NM_VOTAVEL"])

df_tmp = df_tmp["QT_VOTOS"].sum().reset_index(name='QT_VOTOS')

df_tmp = df_tmp.sort_values(by=["QT_VOTOS"], ascending=False).reset_index(drop=True)

df_tmp = df_tmp[0:40]

df_tmp["QT_VOTOS_PERCENTUAL"] = (df_tmp["QT_VOTOS"] / qnt_votos_validos_cargo_verador) * 100

df_vereadores = df_tmp

st.dataframe(df_vereadores)

st.write("#### Quantidade Total de Votos em validos, branco, nulo e anulados:")

df_tmp = df.loc[(df['NR_VOTAVEL'].isin([95, 96, 97])), ['NM_VOTAVEL','NR_NM_VOTAVEL','QT_VOTOS']]

df_tmp = df_tmp.groupby(["NM_VOTAVEL","NR_NM_VOTAVEL"])

df_tmp = df_tmp["QT_VOTOS"].sum().reset_index(name='QT_VOTOS')

df_tmp = df_tmp.sort_values(by=["QT_VOTOS"], ascending=False).reset_index(drop=True)

df_tmp["QT_VOTOS_PERCENTUAL"] = (df_tmp["QT_VOTOS"] / df["QT_VOTOS"].sum()) * 100

df_branco_nulos = df_tmp

new_record = pd.DataFrame([
    {   
        'NM_VOTAVEL': 'VALIDOS PREFEITO',
        'NR_NM_VOTAVEL': '93 - VALIDOS PREFEITO', 
        'QT_VOTOS': qnt_votos_validos_cargo_prefeito, 
        'QT_VOTOS_PERCENTUAL': ((qnt_votos_validos_cargo_prefeito/qnt_total_de_votos)* 100)
    },
    {
        'NM_VOTAVEL': 'VALIDOS VEREADOR',
        'NR_NM_VOTAVEL': '94 - VALIDOS VEREADOR', 
        'QT_VOTOS': qnt_votos_validos_cargo_verador, 
        'QT_VOTOS_PERCENTUAL': ((qnt_votos_validos_cargo_verador/qnt_total_de_votos)* 100)
    }])

df_branco_nulos = pd.concat([df_tmp, new_record], ignore_index=True)

st.dataframe(df_branco_nulos)

st.divider()

################################################################
# Sessão de Gráficos

st.write("# Sessão de gráficos")

st.write("## Quantidade Total de Votos de cada candidato a Prefeito em %")

num_top_candidatos = 4

df_prefeito_pie = df_prefeito

if len(df_prefeito_pie) > num_top_candidatos:
    df_tmp_top = df_prefeito_pie.iloc[:num_top_candidatos].copy()
    outros = df_prefeito_pie.iloc[num_top_candidatos:]['QT_VOTOS'].sum()
    outros_p = df_prefeito_pie.iloc[num_top_candidatos:]['QT_VOTOS_PERCENTUAL'].sum()
    new_record = pd.DataFrame([{
        'NR_VOTAVEL': 99 , 
        'NR_NM_VOTAVEL': 'Outros', 
        'QT_VOTOS': outros, 
        'QT_VOTOS_PERCENTUAL': outros_p}])
    df_prefeito_pie = pd.concat([df_tmp_top, new_record], ignore_index=True)
else:
    df_prefeito_pie = df_prefeito

# Criar o gráfico de área estilo pie
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(df_prefeito_pie["QT_VOTOS_PERCENTUAL"], autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Para o gráfico ficar circular

# Criar a legenda separada
ax.legend(wedges, df_prefeito_pie['NR_NM_VOTAVEL'],
          title="Candidatos a Prefeito",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

st.write("## Quantidade Total de Votos dos 40 vereadores mais bem votas em %")

df_vereadores_pie = df_vereadores

# Geração dinâmica das cores usando um mapa de cores
colormap = plt.cm.viridis  # Escolha o mapa de cores que você prefere (há vários disponíveis)
cores = [colormap(i) for i in np.linspace(0, 1, len(df_vereadores_pie))]

# Calcular a média móvel de 3 meses
media_movel = pd.Series(df_vereadores_pie['QT_VOTOS_PERCENTUAL']).rolling(window=3).mean().tolist()

# Criar o gráfico de barras
fig, ax1 = plt.subplots()
bars = ax1.bar(df_vereadores_pie['NR_NM_VOTAVEL'], df_vereadores_pie['QT_VOTOS_PERCENTUAL'], color=cores)
ax1.set_title('Gráfico de Barras')
ax1.set_xlabel('NR_NM_VOTAVEL')
ax1.set_ylabel('QT_VOTOS_PERCENTUAL')
ax1.tick_params(axis='x', rotation=90)

# # Definir a legenda separada
# ax.legend(bars, df['NR_NM_VOTAVEL'], title="NR_NM_VOTAVEL", loc="best", bbox_to_anchor=(1, 1))

# Criar um segundo eixo y para o gráfico de linha
ax2 = ax1.twinx()
ax2.plot(df_vereadores_pie['NR_NM_VOTAVEL'], media_movel, color='red', marker='o', label='Média Móvel')
ax2.set_ylabel('Média Móvel', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

st.write("## Percentual de votos brancos, nulos, anulados, votos validos para cargo de Vereador")

# Criar o gráfico de área estilo pie
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(df_branco_nulos["QT_VOTOS_PERCENTUAL"], autopct='%1.1f%%', startangle=90)
# Para o gráfico ficar circular
ax.axis('equal')  

# Criar a legenda separada
ax.legend(wedges, df_branco_nulos['NM_VOTAVEL'],
          title="Tipo de Votos",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

# Mostrar o gráfico no Streamlit
st.pyplot(fig)
