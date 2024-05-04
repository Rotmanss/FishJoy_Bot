import networkx as nx
import matplotlib.pyplot as plt

from best_visiting_route.calculate_distance import haversine


def create_graph(coordinates):
    G = nx.Graph()
    distance_matrix = []

    for lat, lon in coordinates:
        G.add_node(f'{lat:.1f}, {lon:.1f}')

    diagonal_index = 0
    for lat1, lon1 in coordinates:
        node_distances = []
        for lat2, lon2 in coordinates:
            if (lat1, lon1) != (lat2, lon2):
                distance = haversine((lat1, lon1), (lat2, lon2))
                distance = round(distance, 1)
                node_distances.append(distance)

                G.add_edge(f'{lat1:.1f}, {lon1:.1f}', f'{lat2:.1f}, {lon2:.1f}', weight=distance)

        node_distances.insert(diagonal_index, 0)
        diagonal_index += 1
        distance_matrix.append(node_distances)

        # draw_graph(G)

    return distance_matrix


def draw_graph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=200, node_color='skyblue', font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()
