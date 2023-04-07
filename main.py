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
for iteration in range(num_iterations):
    for ant in range(num_ants):
        current_city = random.randint(0, len(distances) - 1)
        visited_cities = [current_city]
        while len(visited_cities) < len(distances):
            probabilities, unvisited_cities = calculate_probabilities(current_city, visited_cities)
            next_city = choose_next_city(probabilities, unvisited_cities)
            visited_cities.append(next_city)
            current_city = next_city
        distance = calculate_distance(visited_cities)
        if distance < best_distance:
            best_solution = visited_cities
            best_distance = distance
        delta_pheromones = np.zeros_like(distances)
        for i in range(len(visited_cities) - 1):
            current_city = visited_cities[i]
            next_city = visited_cities[i + 1]
            delta_pheromones[current_city, next_city] += 1 / distance
            delta_pheromones
