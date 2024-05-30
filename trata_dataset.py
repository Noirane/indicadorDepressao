import pandas as pd

# Lista das colunas desejadas
selected_columns = ['Q3A', 'Q5A', 'Q10A', 'Q13A', 'Q16A', 'Q17A', 'Q21A', 'Q24A', 'Q26A', 'Q31A', 'Q34A', 'Q37A', 'Q38A', 'Q42A', 'gender',
                    'country', 'education', 'age', 'religion', 'orientation', 'married', 'familysize']

# Caminho do arquivo original e novo arquivo CSV
file_path = 'data.csv'
new_file_path = 'selected_data.csv'

# Carrega o DataFrame original do arquivo CSV
df = pd.read_csv(file_path)

# Cria um novo DataFrame com as colunas selecionadas
new_df = df[selected_columns]

# Salva o novo DataFrame no novo arquivo CSV
new_df.to_csv(new_file_path, index=False)
