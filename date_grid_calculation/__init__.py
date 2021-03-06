from database import query_db, commit_many
import numpy as np
from progressbar import progress


def closest_node(node, nodes):
    nodes = np.asarray(nodes)
    dist_2 = np.sum((nodes - node)**2, axis=1)
    return nodes[np.argmin(dist_2)]


def date_grid_calculation():
    dates = query_db('SELECT DateID, Azimut, Elevation FROM Date')
    grid = [(row[0], row[1]) for row in query_db('SELECT Azimut, Elevation FROM Grid')]
    data = []
    i = 0
    i_max = len(dates)
    for row in dates:
        point = (row[1], row[2])
        closest = closest_node(point, grid)
        data.append((closest[0], closest[1], row[0]))
        i += 1
        progress(i, i_max)

    commit_many('UPDATE Date SET GridID = (SELECT GridID FROM Grid WHERE Grid.Azimut = ? AND Grid.Elevation = ?) '
                'WHERE DateID = ?', data)
    return
