from best_visiting_route.calculate_distance import haversine


class KNearestNeighbours:
    def __init__(self, k=3):
        self.k = k
        self.point = None

    def fit(self, points):
        self.points = points

    def predict(self, new_point):
        distances = []

        for point in self.points:
            distance = haversine(point, new_point)
            distances.append((distance, point))

        top_distances = [top[0] for top in sorted(distances)[:self.k]]
        return {'all_distances_and_coords': distances, 'top_distances': top_distances}
