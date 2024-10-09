import streamlit as st
import pandas as pd
import plotly.express as px
import country_data  
from tabel import create_table

def level_layout(df, selected_country):
    # Definindo os níveis de depressão e suas cores
    levels = {
        0: ("Normal", "white"),
        1: ("Mild", "#FDFD96"),  # Amarelo claro
        2: ("Moderate", "#FFA500"),  # Laranja
        3: ("Severe", "#FF6F00"),  # Laranja escuro
        4: ("Extremely Severe", "#ED3419")  # Vermelho escuro
    }

    # Definindo as cores dos gêneros
    gender_colors = {
        'Male': '#1f77b4',  # Azul
        'Female': '#ff69b4',  # Rosa
        'Other': '#6a0dad'      # Roxo
    }

     # Definindo os rótulos de education
    education_labels = {
        1: 'Less than high school',
        2: 'High school',
        3: 'University degree',
        4: 'Graduate degree'
    }

     # Definindo os rótulos de married
    married_labels = {
        1: 'Never married',
        2: 'Currently married',
        3: 'Previously married'
    }

    # Lida com a seleção "All Countries"
    if selected_country == 'All Countries':
        country_df = df  # Usa o DataFrame completo
        country_participants = country_df.shape[0]
    else:
        # Converte o nome do país selecionado em seu número correspondente
        country_number = next(key for key, value in country_data.country_mapping.items() if value == selected_country)
        # Filtra o dataframe com base no país selecionado
        country_df = df[df['country'] == country_number]
        country_participants = country_df.shape[0]

  

    # Definir o estilo para as caixas
    box_style = """
    <style>
    .box {
        border: 1px solid #d3d3d3;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        background-color: transparent;
    }
    .box-large-font {
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(box_style, unsafe_allow_html=True)

    # Caixa com o total de participantes
    st.markdown(
        f'<div class="box">Total participants: <span class="box-large-font">{country_participants}</span><br>Average depression score: {country_df["indice_depressao"].mean():.2f}</div>',
        unsafe_allow_html=True
    )

    # Gráfico de pizza 3D para distribuição de gênero
    gender_counts = country_df['gender'].value_counts().reindex([1, 2, 3], fill_value=0)
    gender_labels = {1: 'Male', 2: 'Female', 3: 'Other'}
    gender_counts.index = [gender_labels[i] for i in gender_counts.index]

    # Calcular porcentagens e médias de níveis de depressão por gênero
    level_data = []
    hover_data = []
    for gender, label in gender_labels.items():
        gender_group = country_df[country_df['gender'] == gender]
        total_gender = gender_group.shape[0]
        if total_gender > 0:
            level_counts = gender_group['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression = gender_group['indice_depressao'].mean()
            hover_info = [f'{levels[level][0]}: {level_counts.get(level, 0):.1f}%' for level in range(5)]
            hover_info.append(f'Average Depression Index: {avg_depression:.2f}')
            hover_data.append('<br>'.join(hover_info))
            for level, count in level_counts.items():
                level_data.append({
                    'Gender': label,
                    'Level': levels[level][0],
                    'Percentage': count
                })

    # Criar o DataFrame para o gráfico de barras
    level_df = pd.DataFrame(level_data)

    # Gráfico de pizza para a distribuição de gênero
    fig_gender = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title='Distribution by gender',
        hole=0.3,
        color=gender_counts.index,
        color_discrete_map=gender_colors,
        labels={'names': 'Gender', 'values': 'Number of Participants'}
    )
    fig_gender.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data,
        pull=[0.1, 0.1, 0.1]
    )
    fig_gender.update_layout(showlegend=True)
    st.plotly_chart(fig_gender, use_container_width=True)

    # Adicionando o gráfico de porcentagem de níveis de depressão por gênero
    gender_level_data = []

    for gender, label in gender_labels.items():
        gender_group_df = country_df[country_df['gender'] == gender]
        total_gender = gender_group_df.shape[0]
        if total_gender > 0:
            level_counts = gender_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            absolute_counts = gender_group_df['indice_depressao'].value_counts().reindex(range(5), fill_value=0)  # Contagem absoluta
            for level, count in level_counts.items():
                gender_level_data.append({
                    'Gender': label,
                    'Level': levels[level][0],
                    'Percentage': "{:.2f}".format(count),
                    'Count': absolute_counts[level]  # Adiciona a contagem
                })

    gender_level_df = pd.DataFrame(gender_level_data)

    # Criação do gráfico
    fig_gender_level = px.bar(
        gender_level_df,
        x='Gender',
        y='Percentage',
        color='Level',
        text='Percentage',  # Mantém o texto de porcentagem no gráfico
        title='Percentage of Depression Levels by Gender',
        labels={'Gender': 'Gender', 'Percentage': 'Percentage'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level']  # Adiciona 'Count' e 'Level' ao custom data
    )

    # Atualizando hovertemplate para mostrar na ordem: Gender, Level, Percentage, Count
    fig_gender_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        textposition='inside',  # Mantém a porcentagem visível
        hovertemplate=(
            "<b>Gender: %{x}</b><br>"
            "Level: %{customdata[1]}<br>"
            "Percentage: %{y:.2f}%<br>"
            "Count: %{customdata[0]}<br>"
            "<extra></extra>"
        )
    )

    fig_gender_level.update_layout(barmode='stack')

    st.plotly_chart(fig_gender_level, use_container_width=True)






        # Agrupando idades em intervalos de 10 anos
    age_bins = list(range(18, 48, 10)) + [48, float('inf')]
    age_labels = [f'{i}-{i+9}' for i in range(18, 48, 10)] + ['48+']
    country_df['age_group'] = pd.cut(country_df['age'], bins=age_bins, labels=age_labels, right=False)

    # Gráfico de pizza para a distribuição de idade
    age_counts = country_df['age_group'].value_counts().sort_index()

    # Definindo as cores vibrantes para as faixas etárias
    age_colors = {
        '18-27': '#77DD77',
        '28-37': '#FF33A8',
        '38-47': '#3357FF',
        '48+': '#D3D3D3',
    }

    # Calculando porcentagens de níveis de depressão e a média por grupo etário
    hover_data_age = []
    age_avg_depression = country_df.groupby('age_group')['indice_depressao'].mean()

    for age_group in age_labels:
        age_group_df = country_df[country_df['age_group'] == age_group]
        total_in_group = age_group_df.shape[0]
        if total_in_group > 0:
            level_counts_age = age_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            hover_info_age = [f'{levels[level][0]}: {level_counts_age.get(level, 0):.1f}%' for level in range(5)]
            hover_info_age.append(f'Average Depression Index: {age_avg_depression[age_group]:.2f}')
            hover_data_age.append('<br>'.join(hover_info_age))
        else:
            hover_data_age.append('No data available')

    # Criando o gráfico de pizza para a distribuição de idade
    fig_age = px.pie(
        names=age_counts.index,
        values=age_counts.values,
        title='Age distribution',
        hole=0.3,
        color=age_counts.index,
        color_discrete_map=age_colors,
        labels={'names': 'Faixa Etária', 'values': 'Número de Participantes'}
    )

    # Atualizando hovertemplate para incluir a média do índice de depressão e "pull" para efeito de salto
    fig_age.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data_age,  # Passando os dados customizados para o hover
        pull=[0.1] * len(age_counts)  # Puxando as fatias para fora (efeito de "salto")
    )

    # Exibindo o gráfico
    st.plotly_chart(fig_age, use_container_width=True)


        # Gráfico de porcentagem de níveis de depressão por idade
    age_level_data = []

    for age_group in age_labels:
        age_group_df = country_df[country_df['age_group'] == age_group]
        total_in_group = age_group_df.shape[0]
        if total_in_group > 0:
            level_counts = age_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression = age_group_df['indice_depressao'].mean()  # Calcular média do índice de depressão
            for level, count in level_counts.items():
                age_level_data.append({
                    'Age Group': age_group,
                    'Level': levels[level][0],  # O nome do nível
                    'Level Name': levels[level][0],  # Armazena o nome do nível
                    'Percentage': count,
                    'Count': age_group_df['indice_depressao'].value_counts().get(level, 0),  # Contagem real de cada nível
                    
                })

    # Criando o DataFrame
    age_level_df = pd.DataFrame(age_level_data)

    # Criando o gráfico de barras
    fig_age_level = px.bar(
        age_level_df,
        x='Age Group',
        y='Percentage',
        color='Level',
        text='Percentage',
        title='Percentage of Depression Levels by Age',
        labels={'Age Group': 'Age', 'Percentage': 'Percentage'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level Name']  # Adiciona o Level Name para custom data
    )

    # Atualizando hovertemplate para incluir contagem e média do índice de depressão
    fig_age_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        texttemplate='%{text:.1f}%', 
        textposition='inside',
        hovertemplate="<b>%{x}</b><br>Level: %{customdata[1]}<br>Percentage: %{y:.2f}%<br>Count: %{customdata[0]}<br><extra></extra>",
    )

    fig_age_level.update_layout(barmode='stack')

    # Exibindo o gráfico
    st.plotly_chart(fig_age_level, use_container_width=True)

     # Gráfico de pizza para a distribuição de educação
    education_counts = country_df['education'].value_counts().reindex([1, 2, 3, 4], fill_value=0)
    education_counts.index = [education_labels[i] for i in education_counts.index]

    # Definindo as cores personalizadas para os níveis de educação  
    education_colors = {
        'Less than high school': '#FF5733',  # Vermelho vibrante
        'High school': '#33FF57',           # Verde vibrante
        'University degree': '#3357FF',     # Azul vibrante
        'Graduate degree': '#FF33A8'        # Rosa vibrante
    }


    # Gráfico de pizza para a distribuição de educação
    education_counts = country_df['education'].value_counts().reindex([1, 2, 3, 4], fill_value=0)
    education_counts.index = [education_labels[i] for i in education_counts.index]

    # Definindo as cores personalizadas para os níveis de educação  
    education_colors = {
        'Less than high school': '#FF5733',  # Vermelho vibrante
        'High school': '#33FF57',             # Verde vibrante
        'University degree': '#3357FF',       # Azul vibrante
        'Graduate degree': '#FF33A8'          # Rosa vibrante
    }

    # Criando o gráfico de pizza para a distribuição de educação
    fig_education = px.pie(
        names=education_counts.index,
        values=education_counts.values,
        title='Distribution by Education',
        hole=0.3,
        color=education_counts.index,
        color_discrete_map=education_colors,
        labels={'names': 'Nível de Educação', 'values': 'Número de Participantes'}
    )

    # Calcular porcentagens e médias de níveis de depressão por educação
    hover_data_education = []
    for education, label in education_labels.items():
        education_group = country_df[country_df['education'] == education]
        total_education = education_group.shape[0]
        if total_education > 0:
            level_counts_education = education_group['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression_education = education_group['indice_depressao'].mean()
            hover_info_education = [f'{levels[level][0]}: {level_counts_education.get(level, 0):.1f}%' for level in range(5)]
            hover_info_education.append(f'Average Depression Index: {avg_depression_education:.2f}')
            hover_data_education.append('<br>'.join(hover_info_education))
        else:
            hover_data_education.append('No data available')

    # Adicionando personalizações para hover e efeito de "pull" das fatias
    fig_education.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data_education,
        pull=[0.1] * len(education_counts)   # Puxando todas as fatias para fora, similar ao gráfico de gênero
     
    )
       

    # Atualizando o layout para exibir a legenda e deixar o gráfico com o mesmo estilo visual
    fig_education.update_layout(
        showlegend=True,
        legend_title_text='Nível de Educação'
    )

    # Exibindo o gráfico
    st.plotly_chart(fig_education, use_container_width=True)




    # Adicionando o gráfico de porcentagem de níveis de depressão por educação
    education_level_data = []

    for education, label in education_labels.items():
        education_group_df = country_df[country_df['education'] == education]
        total_in_group = education_group_df.shape[0]
        if total_in_group > 0:
            level_counts = education_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            absolute_counts = education_group_df['indice_depressao'].value_counts().reindex(range(5), fill_value=0)  # Contagem absoluta
            for level, count in level_counts.items():
                education_level_data.append({
                    'Education': label,
                    'Level': levels[level][0],
                    'Percentage': "{:.2f}".format(count),
                    'Count': absolute_counts[level],  # Adiciona a contagem absoluta
                    'Level Name': levels[level][0]  # Adiciona o nome do nível
                })

    # Criando o DataFrame
    education_level_df = pd.DataFrame(education_level_data)

    # Criando o gráfico de barras
    fig_education_level = px.bar(
        education_level_df,
        x='Education',
        y='Percentage',
        color='Level',
        text='Percentage',  # Adiciona o texto de porcentagem
        title='Percentage of Depression Levels by Education',
        labels={'Education': 'Nível de Educação', 'Percentage': 'Porcentagem'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level Name']  # Adiciona o Level Name para custom data
    )

    # Atualizando hovertemplate para incluir contagem e nome do nível
    fig_education_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        texttemplate='%{text:.1f}%', 
        textposition='inside',
        hovertemplate="<b>%{x}</b><br>Level: %{customdata[1]}<br>Percentage: %{y:.2f}%<br>Count: %{customdata[0]}<br><extra></extra>"
    )

    fig_education_level.update_layout(barmode='stack')

    # Exibindo o gráfico
    st.plotly_chart(fig_education_level, use_container_width=True)


   
   # Gráfico de pizza para a distribuição de estado civil
    married_counts = country_df['married'].value_counts().reindex([1, 2, 3], fill_value=0)
    married_counts.index = [married_labels[i] for i in married_counts.index]

    married_colors = {
        'Never married': '#40e0d0',    # Vermelho vibrante
        'Currently married': '#33FF57',      # Verde vibrante
        'Previously married': '#db0075'   # Azul vibrante
    }

    # Criando o gráfico de pizza para a distribuição de estado civil
    fig_married = px.pie(
        names=married_counts.index,
        values=married_counts.values,
        title='Distribution by Civil Status',
        hole=0.3,
        color=married_counts.index,
        color_discrete_map=married_colors,
        labels={'names': 'Marital status', 'values': 'Number of Participants'}
    )

   

    # Calcular porcentagens e médias de níveis de depressão por estado civil
    hover_data_married = []
    for married, label in married_labels.items():
        married_group = country_df[country_df['married'] == married]
        total_married = married_group.shape[0]
        if total_married > 0:
            level_counts_married = married_group['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            avg_depression_married = married_group['indice_depressao'].mean()
            hover_info_married = [f'{levels[level][0]}: {level_counts_married.get(level, 0):.1f}%' for level in range(5)]
            hover_info_married.append(f'Average Depression Index: {avg_depression_married:.2f}')
            hover_data_married.append('<br>'.join(hover_info_married))
        else:
            hover_data_married.append('No data available')

    # Adicionando personalizações para hover e efeito de "pull" das fatias
    fig_married.update_traces(
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>%{customdata}<extra></extra>",
        customdata=hover_data_married,
        pull=[0.1] * len(married_counts)  # Puxando todas as fatias para fora
    )

   

    # Atualizando o layout para exibir a legenda e manter o mesmo estilo visual do gráfico de "Education"
    fig_married.update_layout(
        showlegend=True,
        legend_title_text='Marital Status'
    )

    # Exibindo o gráfico
    st.plotly_chart(fig_married, use_container_width=True)


        # Gráfico de porcentagem de níveis de depressão por estado civil
    married_level_data = []

    for married, label in married_labels.items():
        married_group_df = country_df[country_df['married'] == married]
        total_in_group = married_group_df.shape[0]
        if total_in_group > 0:
            level_counts = married_group_df['indice_depressao'].value_counts(normalize=True).reindex(range(5), fill_value=0) * 100
            absolute_counts = married_group_df['indice_depressao'].value_counts().reindex(range(5), fill_value=0)  # Contagem absoluta
            for level, count in level_counts.items():
                married_level_data.append({
                    'Marital Status': label,
                    'Level': levels[level][0],  # O nome do nível
                    'Percentage': "{:.2f}".format(count),
                    'Count': absolute_counts[level]  # Adiciona a contagem absoluta
                })

    # Criando o DataFrame
    married_level_df = pd.DataFrame(married_level_data)

    # Criando o gráfico de barras
    fig_married_level = px.bar(
        married_level_df,
        x='Marital Status',
        y='Percentage',
        color='Level',
        text='Percentage',  # Adiciona o texto de porcentagem
        title='Percentage of Depression Levels by Marital Status',
        labels={'Marital Status': 'Marital Status', 'Percentage': 'Percentage'},
        color_discrete_map={val[0]: val[1] for val in levels.values()},
        custom_data=['Count', 'Level']  # Adiciona a contagem e o nível para custom data
    )

    # Atualizando hovertemplate para incluir contagem e nome do nível
    fig_married_level.update_traces(
        marker=dict(line=dict(color='black', width=1)),
        texttemplate='%{text:.1f}%', 
        textposition='inside',
        hovertemplate="<b>%{x}</b><br>Level: %{customdata[1]}<br>Percentage: %{y:.2f}%<br>Count: %{customdata[0]}<br><extra></extra>"
    )

    fig_married_level.update_layout(barmode='stack')

    # Exibindo o gráfico
    st.plotly_chart(fig_married_level, use_container_width=True)



def show_country_details():
    # Carregue o conjunto de dados
    df = pd.read_csv('dataset.csv')

    # Crie a lista de países
    countries = ['Select Country']+['All Countries'] + [country for country in country_data.country_mapping.values()]

    # Seleção de caixa apenas para países
    selected_country = st.selectbox('', countries, key='select_country')

    # Use st.markdown() com HTML e CSS para definir uma fonte personalizada (somente uma vez)
    st.markdown(
        """
        <style>
        .custom-title {
            font-size: 20px;
            font-weight: bold;
        }
        </style>
        
        """, 
        unsafe_allow_html=True
    )

   
    if selected_country != 'Select Country':
        # Chama a função para mostrar detalhes do país selecionado
        level_layout(df, selected_country)
        
        # Injetando CSS personalizado
        st.markdown(
            """
            <style>
            .custom-title {
                font-size: 22px;  /* Ajuste o tamanho conforme necessário */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Usando a classe personalizada no título
        st.markdown('<h1 class="custom-title">Resume</h1>', unsafe_allow_html=True)
        
        # Cria a tabela para o país selecionado
        create_table(selected_country)

    
