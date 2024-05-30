import streamlit as st
import pandas as pd
from gera_grafico import generate_pie_chart
from localiza_participante import localizar_participante
from soma import calcular_soma, mapear_indice_depressao  # Importe as funções do arquivo soma.py

st.title('Indicadores de depressão')

# Função para carregar os dados
def load_data(file):
    data = pd.read_csv(file)
    # Preservar nomes originais das colunas
    original_columns = data.columns
    # Converter nomes das colunas para minúsculas para manipulação
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data, original_columns

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")


if uploaded_file is not None:
    data, original_columns = load_data(uploaded_file)
    st.subheader('Dados brutos')
    # Verifique se as colunas existem antes de chamar a função calcular_soma
    try:
        data = calcular_soma(data)
        # Aplicar a função mapear_indice_depressao à coluna soma_depressao
        data['indice_depressao'] = data['soma_depressao'].apply(mapear_indice_depressao)
    except KeyError as e:
        st.error(f"Erro: {e}")
    else:
        # Restaurar nomes originais das colunas e adicionar novas colunas
        data.columns = list(original_columns) + ['soma_depressao', 'indice_depressao']
        st.write(data)
    
    localizar_participante(data)
 
   

    # Gera o gráfico de pizza usando a função do arquivo separado
    fig = generate_pie_chart(data)

    if fig is not None:
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)
    else:
        st.error("O arquivo CSV não contém a coluna 'gender' necessária para gerar o gráfico.")
