from database import get_polygons, get_shortest, commit_many
from shapely.geometry import Polygon, LineString
from shapely.geos import TopologicalError


def get_weight(edge, nodes, polygons):
    line = LineString([nodes[edge[0]], nodes[edge[1]]])
    length = line.length
    length_shadow = 0.
    i = 0
    for poly in polygons:
        i += 1
        try:
            inter = line.intersection(Polygon(poly))
            if not inter.is_empty:
                length_shadow += inter.length
        except TopologicalError:
            polygons.remove(poly)
    return 10.-(9.*(length_shadow / length))


def insert_graph(grid_id):
    polygons = get_polygons(grid_id)
    shortest, nodes = get_shortest()

    data = []
    for edge in shortest:
        factor = get_weight(edge, nodes, polygons)
        data.append((grid_id, edge[0], edge[1], edge[2] * factor, factor))

    commit_many('INSERT INTO Graph(GridID, FromID, ToID, Costs, Factor) VALUES (?, ?, ?, ?, ?)', data)
    print 'Finished GridID: ' + str(grid_id)
    return
