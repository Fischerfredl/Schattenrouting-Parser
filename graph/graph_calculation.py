from database import get_polygons, get_graph, commit_many, get_bounds_buildings
from shapely.geometry import Polygon, LineString, MultiPolygon
from shapely.ops import unary_union
from shapely.geos import TopologicalError
from shapely import speedups
from progressbar import progress

speedups.enable()


def get_weight(edge, nodes, polygons, bb=get_bounds_buildings()):
    line = LineString([nodes[edge[1]], nodes[edge[2]]])

    if line.intersection(Polygon(bb)).is_empty:
        return 10

    line_length = line.length
    shadow_length = 0.
    try:
        for poly in polygons:
            inter = line.intersection(poly)
            shadow_length += inter.length
            if shadow_length == line_length:
                break
    except TopologicalError as e:
        print 'Intersection Calculation failed at Graph-ID: ' + str(edge[0])
        print e.message
        return 10
    return 10.-(9.*(shadow_length / line.length))


def insert_graph(grid_id):
    try:
        polygons = unary_union(get_polygons(grid_id))
        if polygons.geom_type != 'MultiPolygon':
            polygons = MultiPolygon(polygons)
        print str(grid_id) + ': Polygons merged'
        shortest, nodes = get_graph()

        data = []
        # i = 0
        for edge in shortest:
            factor = get_weight(edge, nodes, polygons)
            data.append((grid_id, edge[0], factor))
            # i += 1
            # if i % 100 == 0:
            #     print str(grid_id) + ': ' + str(i)
        commit_many('INSERT INTO Weighted(GridID, GraphID, Factor) VALUES (?, ?, ?)', data)
        print 'Finished GridID: ' + str(grid_id)
    except ValueError as e:
        print 'Failed at Grid-ID: ' + str(grid_id)
        print e.message
    return
