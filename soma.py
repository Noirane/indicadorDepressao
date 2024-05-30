# soma.py
def calcular_soma(data):
    perguntas_depressao = ['q3a', 'q5a', 'q10a', 'q13a', 'q16a', 'q17a', 'q21a', 'q24a', 'q26a', 'q31a', 'q34a', 'q37a', 'q38a', 'q42a']
    data['soma_depressao'] = data[perguntas_depressao].sum(axis=1)
    return data

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