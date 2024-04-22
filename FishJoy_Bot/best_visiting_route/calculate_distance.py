from math import sin, asin, sqrt, cos, radians


def haversine(p1, p2):
    lon1, lat1, lon2, lat2 = map(radians, [*p1, *p2])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    # 'a' is the square of half the chord length between the points on the Earth's surface.
    a = sin(delta_lat/2)**2 + cos(lat1) * cos(lat2) * sin(delta_lon/2)**2

    # 'c' is the angular distance between the points along the surface of a unit sphere.
    c = 2 * asin(sqrt(a))

    earth_radius = 6367
    dist = earth_radius * c

    return dist
