import streamlit as st

def localizar_participante(data):
    st.subheader('Localizar participante pelo índice')
    index = st.number_input('Insira o índice da linha:', min_value=0, max_value=len(data)-1, step=1)

    if st.button('Mostrar linha'):
        if 0 <= index < len(data):
            st.write(data.iloc[[index]])
        else:
            st.write('Índice fora do intervalo.')
