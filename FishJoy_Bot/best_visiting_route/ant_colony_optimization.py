import random
import numpy as np


# Distance between each pair of nodes
# distance_matrix = [[0, 123, 248],
#                    [123, 0, 113],
#                    [248, 113, 0]]
# num_nodes = 3

distance_matrix = []

num_nodes = 0

num_ants = 5
alpha = 1.0  # Pheromone importance
beta = 2.0  # Distance importance
evaporation_rate = 0.5
pheromone_deposit = 1.0
num_iterations = 5000

pheromone_level = []


def init_values(value):
    global distance_matrix
    distance_matrix = value
    print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQ matrix\n', np.array(distance_matrix))

    global num_nodes
    num_nodes = len(value[0])

    global pheromone_level
    pheromone_level = [[1.0] * num_nodes for _ in range(num_nodes)]


def tour_length(tour):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i]][tour[i + 1]]
    total_distance += distance_matrix[tour[-1]][tour[0]]  # Return to the starting node
    return total_distance


class Ant:
    def __init__(self):
        self.visited = [False] * num_nodes
        self.tour = []

    def choose_next_node(self, current_node):
        unvisited_nodes = [i for i in range(num_nodes) if not self.visited[i]]
        probabilities = [0] * len(unvisited_nodes)
        total_probability = 0

        for i, node in enumerate(unvisited_nodes):
            pheromone = pheromone_level[current_node][node]
            distance = distance_matrix[current_node][node]
            probabilities[i] = (pheromone ** alpha) * ((1 / distance) ** beta)
            total_probability += probabilities[i]

        # Roulette wheel selection
        rand = random.uniform(0, total_probability)
        cumulative_probability = 0
        for i, prob in enumerate(probabilities):
            cumulative_probability += prob
            if cumulative_probability >= rand:
                return unvisited_nodes[i]

    def tour_construction(self):
        start_node = random.randint(0, num_nodes - 1)
        self.tour.append(start_node)
        self.visited[start_node] = True

        while False in self.visited:
            current_node = self.tour[-1]
            next_node = self.choose_next_node(current_node)
            self.tour.append(next_node)
            self.visited[next_node] = True


def ant_colony_optimization():
    for iteration in range(num_iterations):
        ants = [Ant() for _ in range(num_ants)]

        for ant in ants:
            ant.tour_construction()

        # Update pheromone levels
        for i in range(num_nodes):
            for j in range(num_nodes):
                if i != j:
                    pheromone_level[i][j] *= (1 - evaporation_rate)  # Evaporation
                    for ant in ants:
                        if j in ant.tour and i in ant.tour:
                            pheromone_level[i][j] += pheromone_deposit / tour_length(ant.tour)

    # Find the best tour
    best_tour = min(ants, key=lambda ant: tour_length(ant.tour)).tour
    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQBest tour:", best_tour)
    print("QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQTour length:", tour_length(best_tour))
