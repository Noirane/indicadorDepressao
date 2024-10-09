# menu.py
import streamlit as st

def display_menu():
    # Sidebar Menu
    st.sidebar.header("Menu")
    
    # Add options to the sidebar menu
    option = st.sidebar.selectbox(
        'Choose an option:',
        ['Home', 'Artificial Intelligence']
    )
    
    # Update the title based on the selected option
    if option == 'Artificial Intelligence':
        st.title("Predicting Depression with Machine Learning")
    elif option == 'Home':
        st.title("Depression Index Map")
    
    return option
