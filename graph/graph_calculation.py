from database import get_polygons, get_graph, commit_many, get_bounds_buildings
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union
from shapely.geos import TopologicalError
from shapely import speedups
from progressbar import progress

speedups.enable()


def get_weight(edge, nodes, polygons, bb):
    line = LineString([nodes[edge[1]], nodes[edge[2]]])
    if line.intersection(bb).is_empty:
        return 10

    shady_lines = []
    for poly in polygons:
        try:
            inter = line.intersection(Polygon(poly))
            if not inter.is_empty:
                if inter.length == line.length:
                    return 1
                shady_lines.append(inter)
        except TopologicalError:
            polygons.remove(poly)
    shadow_length = 0.
    shady = unary_union(shady_lines)
    if shady.geom_type == 'LineString':
        shadow_length = shady.length
    elif shady.geom_type == 'MultiLineString':
        for l in shady:
            shadow_length += l.length
    return 10.-(9.*(shadow_length / line.length))


def insert_graph(grid_id):
    polygons = get_polygons(grid_id)
    shortest, nodes = get_graph()
    bb = Polygon(get_bounds_buildings())

    

    data = []
    for edge in shortest:
        factor = get_weight(edge, nodes, polygons, bb)
        data.append((grid_id, edge[0], factor))

    commit_many('INSERT INTO Weighted(GridID, GraphID, Factor) VALUES (?, ?, ?)', data)
    print 'Finished GridID: ' + str(grid_id)
    return
