import numpy as np

# Define a matriz de distâncias entre as cidades
distancias = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

# Define os parâmetros do algoritmo
quantidade_formiga = 10
maximo_iteracoes = 50
alpha = 1
beta = 2
taxa_evaporacao = 0.5

# Inicializa a matriz de feromônios com valores iguais
feromonios = np.ones_like(distancias)

# Define a função de atualização dos feromônios
def atualizar_feromonios(delta_feromonios):
    global feromonios
    feromonios = (1 - taxa_evaporacao) * feromonios + delta_feromonios

# Define a função para calcular a probabilidade de escolha da próxima cidade
def calculate_probabilidade(cidade_atual, cidades_visitadas):
    cidades_nao_descobertas = np.delete(np.arange(len(distancias)), cidades_visitadas)
    distancias_to_cidades_nao_descobertas = distancias[cidade_atual, cidades_nao_descobertas]
    feromonios_to_cidades_nao_descobertas = feromonios[cidade_atual, cidades_nao_descobertas]
    eta = 1 / distancias_to_cidades_nao_descobertas
    numerador = feromonios_to_cidades_nao_descobertas ** alpha * eta ** beta
    denominador = np.sum(numerador)
    probabilidade = numerador / denominador
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
    for ant in range(quantidade_formiga):
        cidade_inicial = np.random.randint(len(distancias))
        formiga_cidades[ant, 0] = cidade_inicial

# Move as formigas para as próximas cidades
for i in range(1, len(distancias)):
    for ant in range(quantidade_formiga):
        cidade_atual = formiga_cidades[ant, i - 1]
        cidades_visitadas = formiga_cidades[ant, :i]
        probabilidade, cidades_nao_descobertas = calculate_probabilidade(cidade_atual, cidades_visitadas)
        cidade_escolhida = escolher_proxima_cidade(probabilidade, cidades_nao_descobertas)
        formiga_cidades[ant, i] = cidade_escolhida

# Calcula a distância percorrida por cada formiga e atualiza a melhor solução encontrada
for ant in range(quantidade_formiga):
    distancia = calculate_distancia(formiga_cidades[ant])
    if distancia < melhor_distancia:
        melhor_distancia = distancia
        melhor_solucao = formiga_cidades[ant]

# Calcula a matriz de delta feromônios
delta_feromonios.fill(0)
for ant in range(quantidade_formiga):
    for i in range(len(distancias) - 1):
        cidade_atual = formiga_cidades[ant, i]
        proxima_cidade = formiga_cidades[ant, i + 1]
        delta_feromonios[cidade_atual, proxima_cidade] += 1 / distancia
    primeira_cidade = formiga_cidades[ant, 0]
    ultima_cidade = formiga_cidades[ant, -1]
    delta_feromonios[ultima_cidade, primeira_cidade] += 1 / distancia

# Atualiza a matriz de feromônios
atualizar_feromonios(delta_feromonios)
print("Melhor solução encontrada:", melhor_solucao)
print("Distância percorrida:", melhor_distancia)