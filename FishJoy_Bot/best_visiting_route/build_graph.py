import numpy as np

from best_visiting_route.calculate_distance import haversine


def create_graph(coordinates):
    distance_matrix = []

    diagonal_index = 0
    for lat1, lon1 in coordinates:
        node_distances = []
        for lat2, lon2 in coordinates:
            if (lat1, lon1) != (lat2, lon2):
                distance = haversine((lat1, lon1), (lat2, lon2))
                distance = round(distance, 1)
                node_distances.append(distance)

        node_distances.insert(diagonal_index, 0)
        diagonal_index += 1
        distance_matrix.append(node_distances)

    print(np.array(distance_matrix))

    return distance_matrix
