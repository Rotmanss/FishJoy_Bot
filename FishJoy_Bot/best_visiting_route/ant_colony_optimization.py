import numpy as np


class AntColonyOptimization:
    def __init__(self, distance_matrix, num_ants, num_iterations, alpha=1.0, beta=5.0, rho=0.5, pheromone_deposit=100):
        self.distance_matrix = distance_matrix
        self.num_nodes = len(distance_matrix)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.pheromone_deposit = pheromone_deposit
        self.pheromone_matrix = np.ones((self.num_nodes, self.num_nodes))
        self.best_route = None
        self.best_distance = float('inf')

    def run(self):
        for _ in range(self.num_iterations):
            all_routes = self.construct_solutions()
            self.update_pheromones(all_routes)
            self.update_best_route(all_routes)
        return self.best_route

    def construct_solutions(self):
        all_routes = []
        for _ in range(self.num_ants):
            route = self.construct_solution()
            all_routes.append(route)
        return all_routes

    def construct_solution(self):
        route = [0]
        visited = set(route)
        for _ in range(self.num_nodes - 1):
            current_node = route[-1]
            next_node = self.select_next_node(current_node, visited)
            route.append(next_node)
            visited.add(next_node)
        route.append(0)  # return to the start
        return route

    def select_next_node(self, current_node, visited):
        probabilities = np.zeros(self.num_nodes)
        for next_node in range(self.num_nodes):
            if next_node not in visited:
                pheromone = self.pheromone_matrix[current_node][next_node] ** self.alpha
                visibility = (1.0 / self.distance_matrix[current_node][next_node]) ** self.beta
                probabilities[next_node] = pheromone * visibility

        if probabilities.sum() == 0:
            remaining_nodes = list(set(range(self.num_nodes)) - visited)
            next_node = np.random.choice(remaining_nodes)
        else:
            probabilities /= probabilities.sum()
            next_node = np.random.choice(range(self.num_nodes), p=probabilities)
        return next_node

    def update_pheromones(self, all_routes):
        self.pheromone_matrix *= (1 - self.rho)
        for route in all_routes:
            route_distance = self.calculate_route_distance(route)
            pheromone_contribution = self.pheromone_deposit / route_distance
            for i in range(len(route) - 1):
                self.pheromone_matrix[route[i]][route[i + 1]] += pheromone_contribution

    def calculate_route_distance(self, route):
        distance = 0
        for i in range(len(route) - 1):
            distance += self.distance_matrix[route[i]][route[i + 1]]
        return distance

    def update_best_route(self, all_routes):
        for route in all_routes:
            route_distance = self.calculate_route_distance(route)
            if route_distance < self.best_distance:
                self.best_distance = route_distance
                self.best_route = route
