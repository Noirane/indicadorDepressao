import pandas as pd

# Lista das colunas desejadas
selected_columns = ['Q3A', 'Q5A', 'Q10A', 'Q13A', 'Q16A', 'Q17A', 'Q21A', 'Q24A', 'Q26A', 'Q31A', 'Q34A', 'Q37A', 'Q38A', 'Q42A', 
                    'gender', 'country', 'education', 'age', 'married', 'familysize']

# Caminho do arquivo original
file_path = 'originalDataset.csv'

# Carregar o arquivo CSV original e selecionar apenas as colunas desejadas
df = pd.read_csv(file_path, delimiter='\t', usecols=selected_columns)

# Contar o número de linhas antes da limpeza
initial_row_count = len(df)

# Substituir 'NONE' por NaN
df.replace('NONE', pd.NA, inplace=True)

# Contar o número de linhas removidas por critério
lines_removed_per_criteria = {}

# Contar linhas com pelo menos um NaN
lines_with_nan = df.isna().any(axis=1)
lines_removed_per_criteria['Com pelo menos um NaN'] = lines_with_nan.sum()
df = df[~lines_with_nan]

# Filtrar por critérios específicos e contar linhas removidas
criteria = {
    'education': (1, 4),
    'familysize': (1, 100),
    'gender': (1, 3),
    'married': (1, 3),
    'age': (18, 120)
}

# Filtrar e contar linhas removidas por intervalo
for column, (low, high) in criteria.items():
    lines_before = len(df)
    df = df[df[column].between(low, high)]
    lines_removed_per_criteria[f'Fora do intervalo de {low} a {high} em {column}'] = lines_before - len(df)

# Filtrar países com pelo menos 30 participantes antes do mapeamento
country_counts = df['country'].value_counts()
valid_countries = country_counts[country_counts >= 30].index
df = df[df['country'].isin(valid_countries)]

# Cria um mapeamento de siglas para números para a coluna 'country'
country_map = {sigla: idx + 1 for idx, sigla in enumerate(df['country'].dropna().unique())}

# Aplica o mapeamento à coluna 'country'
df['country'] = df['country'].map(country_map)

# Subtrai 1 de cada item nas colunas especificadas
item_columns = ['Q3A', 'Q5A', 'Q10A', 'Q13A', 'Q16A', 'Q17A', 'Q21A', 'Q24A', 'Q26A', 'Q31A', 'Q34A', 'Q37A', 'Q38A', 'Q42A']
df[item_columns] = df[item_columns] - 1

# Adicionar a coluna soma_depressao
perguntas_depressao = item_columns
df['soma_depressao'] = df[perguntas_depressao].sum(axis=1)

# Função para mapear o índice de depressão
def mapear_indice_depressao(pontuacao):
    if pontuacao <= 9:
        return 0
    elif pontuacao <= 13:
        return 1
    elif pontuacao <= 20:
        return 2
    elif pontuacao <= 27:
        return 3
    else:
        return 4

# Adicionar a coluna indice_depressao
df['indice_depressao'] = df['soma_depressao'].apply(mapear_indice_depressao)

# Contar o número de linhas após a limpeza
final_row_count = len(df)

# Calcular o número total de linhas eliminadas
total_lines_removed = initial_row_count - final_row_count

# Exibir os resultados
print(f'Número total de linhas eliminadas: {total_lines_removed}')
print(f'Número de linhas restantes: {final_row_count}')

for criteria, count in lines_removed_per_criteria.items():
    print(f'{criteria}: {count} linhas eliminadas')

# Imprime a legenda para 'country'
print("Legenda para a coluna 'country':")
for country, number in country_map.items():
    print(f"{country}: {number}")

# Selecionar 24.655 linhas aleatórias, se houver pelo menos esse número de linhas restantes
desired_row_count = 24655
if final_row_count >= desired_row_count:
    df_subset = df.sample(n=desired_row_count, random_state=1)  # random_state para reproducibilidade
else:
    df_subset = df

# Salvar o subconjunto em um novo arquivo CSV
df_subset.to_csv('dataset.csv', index=False)

# Exibir o número de linhas no subconjunto salvo
print(f'Número de linhas no subconjunto selecionado: {len(df_subset)}')
