import numpy as np

# Define a matriz de distâncias entre as cidades
distancias = np.array([
    [0, 20, 30, 25, 10, 15, 35, 45, 50, 55],
    [20, 0, 35, 15, 30, 40, 10, 25, 50, 40],
    [30, 35, 0, 45, 20, 25, 50, 15, 10, 30],
    [25, 15, 45, 0, 35, 10, 30, 40, 20, 50],
    [10, 30, 20, 35, 0, 25, 30, 50, 45, 15],
    [15, 40, 25, 10, 25, 0, 20, 30, 55, 35],
    [35, 10, 50, 30, 30, 20, 0, 45, 25, 40],
    [45, 25, 15, 40, 50, 30, 45, 0, 10, 20],
    [50, 50, 10, 20, 45, 55, 25, 10, 0, 30],
    [55, 40, 30, 50, 15, 35, 40, 20, 30, 0]
])

# Parâmetro que controla a influência da trilha de feromônio na escolha da próxima cidade a ser visitada pela formiga.
alpha = 1
# Parâmetro que controla na escolha da próxima cidade a ser visitada pela formiga. 
beta = 2
# Define os parâmetros do algoritmo
quantidade_formiga = 50
taxa_evaporacao = 0.5
maximo_iteracoes = 100

# Inicializa a matriz de feromônios com valores iguais
feromonios = np.ones_like(distancias)

# Define a função de atualização dos feromônios
def atualizar_feromonios(delta_feromonios):
    global feromonios
    feromonios = (1 - taxa_evaporacao) * feromonios + delta_feromonios

# Função usalmente usada em IA para problemas de otimização
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

# Define a função para calcular a probabilidade de escolha da próxima cidade
def calcular_probabilidade(cidade_atual, cidades_visitadas):
    cidades_nao_descobertas = np.delete(np.arange(len(distancias)), cidades_visitadas)
    distancias_to_cidades_nao_descobertas = distancias[cidade_atual, cidades_nao_descobertas]
    feromonios_to_cidades_nao_descobertas = feromonios[cidade_atual, cidades_nao_descobertas]
    eta = 1 / distancias_to_cidades_nao_descobertas
    numerador = feromonios_to_cidades_nao_descobertas ** alpha * eta ** beta
    denominador = np.sum(numerador)
    probabilidade = numerador / denominador
    probabilidade = softmax(probabilidade)
    return probabilidade, cidades_nao_descobertas


# Define a função para escolher a próxima cidade baseada nas probabilidades
def escolher_proxima_cidade(probabilidade, cidades_nao_descobertas):
    cidade_escolhida = np.random.choice(cidades_nao_descobertas, p=probabilidade)
    return cidade_escolhida

# Define a função para calcular a distância total percorrida por uma formiga
def calculate_distancia(cidades_visitadas):
    quantidade_cidades = len(cidades_visitadas)
    distancia = 0
    for i in range(quantidade_cidades - 1):
        cidade_atual = cidades_visitadas[i]
        proxima_cidade = cidades_visitadas[i + 1]
        distancia += distancias[cidade_atual, proxima_cidade]
    distancia += distancias[cidades_visitadas[-1], cidades_visitadas[0]]
    return distancia

# Executa o algoritmo
melhor_solucao = None
melhor_distancia = np.inf
delta_feromonios = np.zeros_like(distancias)
for iteracao in range(maximo_iteracoes):
# Inicializa as formigas em cidades aleatórias
    formiga_cidades = np.zeros((quantidade_formiga, len(distancias)), dtype=int)
    for formiga in range(quantidade_formiga):
        cidade_inicial = np.random.randint(len(distancias))
        formiga_cidades[formiga, 0] = cidade_inicial

# Move as formigas para as próximas cidades
for i in range(1, len(distancias)):
    for formiga in range(quantidade_formiga):
        cidade_atual = formiga_cidades[formiga, i - 1]
        cidades_visitadas = formiga_cidades[formiga, :i]
        probabilidade, cidades_nao_descobertas = calcular_probabilidade(cidade_atual, cidades_visitadas)
        cidade_escolhida = escolher_proxima_cidade(probabilidade, cidades_nao_descobertas)
        formiga_cidades[formiga, i] = cidade_escolhida

# Calcula a distância percorrida por cada formiga e atualiza a melhor solução encontrada
for formiga in range(quantidade_formiga):
    distancia = calculate_distancia(formiga_cidades[formiga])
    if distancia < melhor_distancia:
        melhor_distancia = distancia
        melhor_solucao = formiga_cidades[formiga]
        print("Nova melhor distancia:", melhor_distancia)
        print("Nova melhor solução:", melhor_solucao,"\n")
        

# Calcula a matriz de delta feromônios
# Delta feromonios é a quantidade de feromônio que cada formiga deposita em sua trilha depois de construir uma solução. 
delta_feromonios.fill(0)
for formiga in range(quantidade_formiga):
    for i in range(len(distancias) - 1):
        cidade_atual = formiga_cidades[formiga, i]
        proxima_cidade = formiga_cidades[formiga, i + 1]
        delta_feromonios[cidade_atual, proxima_cidade] += 1 / distancia
    primeira_cidade = formiga_cidades[formiga, 0]
    ultima_cidade = formiga_cidades[formiga, -1]
    delta_feromonios[ultima_cidade, primeira_cidade] += 1 / distancia

# Atualiza a matriz de feromônios
atualizar_feromonios(delta_feromonios)

# Printa os resultados finais
print("========== ENCERRADO ==========")
print("Melhor solução encontrada:", melhor_solucao)
print("Distância percorrida:", melhor_distancia)