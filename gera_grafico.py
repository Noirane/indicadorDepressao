import plotly.express as px

def generate_pie_chart(data):
    # Mapear o campo 'gender' para 'Homem' e 'Mulher' se existir
    if 'gender' in data.columns:
        data['gender'] = data['gender'].map({1: 'Homem', 2: 'Mulher'})

        # Contar a quantidade de homens e mulheres
        gender_counts = data['gender'].value_counts()

        # Criar o gráfico de pizza com Plotly Express
        fig = px.pie(values=gender_counts, names=gender_counts.index, title='Quantidade de Homens e Mulheres')

        return fig
    else:
        return None
