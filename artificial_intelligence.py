import joblib
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.preprocessing import StandardScaler
import json



def graph_models():
    # Carregar o arquivo pkl com os modelos treinados
    modelos_treinados = joblib.load('modelos_treinados.pkl')

    # Extrair e imprimir as métricas de acurácia dos modelos
    resultados = {nome: info['accuracy'] for nome, info in modelos_treinados.items()}

    # Plotar o gráfico de barras
    fig, ax = plt.subplots()
    modelos = list(resultados.keys())
    acuracias = list(resultados.values())
    
    barras = ax.bar(modelos, acuracias, color='orange')
    ax.set_xlabel('Models')
    ax.set_ylabel('Accuracy')
    ax.set_title('Comparison of Model Accuracy')
    
    # Ajustar a rotação dos rótulos do eixo x
    plt.xticks(rotation=45, ha='right')

    # Adicionar o valor da acurácia em cima de cada barra com fonte menor
    for barra in barras:
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2.0, altura, f'{altura * 100:.2f}%', 
                ha='center', va='bottom', fontsize=8)  # Ajuste o tamanho da fonte aqui

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)


def plot_shap_summary():
    # Carregar as informações do gráfico a partir do arquivo JSON
    with open('grafico_info.json', 'r') as f:
        grafico_info = json.load(f)

    # Criar o gráfico de barras com os dados carregados do JSON
    fig, ax = plt.subplots(figsize=grafico_info['figsize'])
    
    ax.barh(grafico_info['features'], grafico_info['mean_abs_shap_values'], color=grafico_info['color'])
    ax.set_xlabel(grafico_info['xlabel'], fontsize=12)
    ax.set_ylabel(grafico_info['ylabel'], fontsize=12)
    ax.set_title(grafico_info['title'], fontsize=14)
    plt.gca().invert_yaxis()  # Inverter o eixo y para mostrar as variáveis mais importantes no topo
    plt.tight_layout()

    # Adicionar rótulos nos valores para cada barra com 4 casas decimais
    for index, value in enumerate(grafico_info['mean_abs_shap_values']):
        ax.text(value, index, f'{value:.4f}', va='center', fontsize=8)  # Ajustado para 4 casas decimais

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)
