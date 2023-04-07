import random
import math
import numpy as np
import matplotlib.pyplot as plt

import random
import numpy as np

# Define a matriz de distâncias entre as cidades
distances = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

# Define os parâmetros do algoritmo
num_ants = 10
num_iterations = 50
alpha = 1
beta = 2
evaporation_rate = 0.5

# Inicializa a matriz de feromônios com valores iguais
pheromones = np.ones_like(distances)

# Define a função de atualização dos feromônios
def update_pheromones(delta_pheromones):
    global pheromones
    pheromones = (1 - evaporation_rate) * pheromones + delta_pheromones

# Define a função para calcular a probabilidade de escolha da próxima cidade
def calculate_probabilities(current_city, visited_cities):
    unvisited_cities = np.delete(np.arange(len(distances)), visited_cities)
    distances_to_unvisited_cities = distances[current_city, unvisited_cities]
    pheromones_to_unvisited_cities = pheromones[current_city, unvisited_cities]
    eta = 1 / distances_to_unvisited_cities
    numerator = pheromones_to_unvisited_cities ** alpha * eta ** beta
    denominator = np.sum(numerator)
    probabilities = numerator / denominator
    return probabilities, unvisited_cities

# Define a função para escolher a próxima cidade baseada nas probabilidades
def choose_next_city(probabilities, unvisited_cities):
    chosen_city = np.random.choice(unvisited_cities, p=probabilities)
    return chosen_city

# Define a função para calcular a distância total percorrida por uma formiga
def calculate_distance(visited_cities):
    num_cities = len(visited_cities)
    distance = 0
    for i in range(num_cities - 1):
        current_city = visited_cities[i]
        next_city = visited_cities[i + 1]
        distance += distances[current_city, next_city]
    distance += distances[visited_cities[-1], visited_cities[0]]
    return distance

# Executa o algoritmo
best_solution = None
best_distance = np.inf
delta_pheromones = np.zeros_like(distances)
for iteration in range(num_iterations):
# Inicializa as formigas em cidades aleatórias
    ant_cities = np.zeros((num_ants, len(distances)), dtype=int)
    for ant in range(num_ants):
        start_city = np.random.randint(len(distances))
        ant_cities[ant, 0] = start_city

# Move as formigas para as próximas cidades
for i in range(1, len(distances)):
    for ant in range(num_ants):
        current_city = ant_cities[ant, i - 1]
        visited_cities = ant_cities[ant, :i]
        probabilities, unvisited_cities = calculate_probabilities(current_city, visited_cities)
        chosen_city = choose_next_city(probabilities, unvisited_cities)
        ant_cities[ant, i] = chosen_city

# Calcula a distância percorrida por cada formiga e atualiza a melhor solução encontrada
for ant in range(num_ants):
    distance = calculate_distance(ant_cities[ant])
    if distance < best_distance:
        best_distance = distance
        best_solution = ant_cities[ant]

# Calcula a matriz de delta feromônios
delta_pheromones.fill(0)
for ant in range(num_ants):
    for i in range(len(distances) - 1):
        current_city = ant_cities[ant, i]
        next_city = ant_cities[ant, i + 1]
        delta_pheromones[current_city, next_city] += 1 / distance
    first_city = ant_cities[ant, 0]
    last_city = ant_cities[ant, -1]
    delta_pheromones[last_city, first_city] += 1 / distance

# Atualiza a matriz de feromônios
update_pheromones(delta_pheromones)
print("Melhor solução encontrada:", best_solution)
print("Distância percorrida:", best_distance)