import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def haversine_distance(point1, point2):
    """
    Oblicza odleglosc miedzy dwoma punktami na powierzchni Ziemi.
    Uzywa wzoru Haversine — poprawny dla wspolrzednych geograficznych.
    Zwraca odleglosc w metrach.
    """
    R = 6371000  # promien Ziemi w metrach

    lat1 = math.radians(point1['latitude'])
    lat2 = math.radians(point2['latitude'])
    delta_lat = math.radians(point2['latitude'] - point1['latitude'])
    delta_lon = math.radians(point2['longitude'] - point1['longitude'])

    a = (math.sin(delta_lat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def solve_tsp(depot, jobs):
    """
    Rozwiazuje TSP przy uzyciu Google OR-Tools.
    Dziala wydajnie dla dziesiatkow i setek punktow.

    depot: dict z kluczami latitude, longitude
    jobs:  lista dictow z kluczami id, latitude, longitude

    Zwraca: lista jobow w optymalnej kolejnosci (bez depotu)
    """
    if not jobs:
        return []

    if len(jobs) == 1:
        return jobs

    # budujemy liste wszystkich punktow: depot na indeksie 0, potem joby
    all_points = [depot] + jobs

    # tworzymy macierz odleglosci — OR-Tools wymaga calkowitych liczb (metry jako int)
    n = len(all_points)
    distance_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                dist = haversine_distance(all_points[i], all_points[j])
                row.append(int(dist))
        distance_matrix.append(row)

    # konfiguracja OR-Tools
    manager = pywrapcp.RoutingIndexManager(n, 1, 0)  # n punktow, 1 pojazd, start w indeksie 0
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # parametry wyszukiwania — PATH_CHEAPEST_ARC to dobry punkt startowy
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    # metaheurystyka GUIDED_LOCAL_SEARCH poprawia wynik po znalezieniu poczatkowego rozwiazania
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_params.time_limit.seconds = 10  # max 10 sekund na szukanie

    solution = routing.SolveWithParameters(search_params)

    if not solution:
        # awaryjnie — jesli OR-Tools nie znajdzie rozwiazania, uzyj greedy
        return _nearest_neighbour(depot, jobs)

    # odczytujemy kolejnosc punktow z rozwiazania
    ordered_jobs = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        if node != 0:  # pomijamy depot (indeks 0)
            ordered_jobs.append(jobs[node - 1])
        index = solution.Value(routing.NextVar(index))

    return ordered_jobs


def _nearest_neighbour(depot, jobs):
    """Heurystyka awaryjna — zawsze idz do najblizszego nieodwiedzonego punktu."""
    unvisited = jobs.copy()
    path = []
    current = depot

    while unvisited:
        nearest = min(unvisited, key=lambda j: haversine_distance(current, j))
        path.append(nearest)
        current = nearest
        unvisited.remove(nearest)

    return path
