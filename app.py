import streamlit as st
import menu  # Imports the menu.py module
import country_details
from artificial_intelligence import graph_models, plot_shap_summary  # Imports the function to display results
from tabel import create_table  # Importa a função create_table

# Function to load the map
def load_map():
    html_file_path = 'mapa_de_calor_com_legenda.html'

    # Read the HTML file content
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Display the HTML content in Streamlit
    st.components.v1.html(html_content, height=600)  # Adjust the height as needed
    # After loading the map, set the loading state
    st.session_state.map_loaded = True

# Check if the session has already started
if 'map_loaded' not in st.session_state:
    st.session_state.map_loaded = False  # Set the initial state

# Display the menu and get the selected option
selected_option = menu.display_menu()

if selected_option == 'Artificial Intelligence':
    # Mostra os gráficos de IA
    graph_models()
    plot_shap_summary()

elif selected_option == 'Home':  # Verifica se a opção Home foi selecionada
    # Carregar o mapa
    load_map()

    # Apenas mostrar os detalhes do país se o mapa foi carregado
    if st.session_state.map_loaded:
        country_details.show_country_details()

    

