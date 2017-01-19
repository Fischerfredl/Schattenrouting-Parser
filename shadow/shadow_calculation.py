from shapely import speedups
from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np
from config import bounds
from database import commit_many, get_buildings, get_grid_info

const = np.pi / 180
speedups.enable()


def transform_point(point, azimut, length):
    delta_lat = np.cos(const*azimut)*length*0.001
    delta_lon = np.sin(const*azimut)*length*0.001
    vektor = (delta_lat/111.3, delta_lon/(111.3*np.cos(const*point[0])))
    return point[0]-vektor[0], point[1]-vektor[1]


def coords_to_array(coords):
    coord_array = []
    for c in coords.strip().split(';'):
        x, y = c.split(',')
        coord_array.append((float(x), float(y)))
    return coord_array


def building_shadow(building, azimut, elevation):
    polygons = []
    coords = coords_to_array(building[0])
    height = building[1]
    length = height / np.tan(const * elevation)
    polygons.append(Polygon(coords))
    for i, item in enumerate(coords[1:], start=1):
        poly = Polygon(
            [coords[i - 1],
             coords[i],
             transform_point(coords[i], azimut, length),
             transform_point(coords[i - 1], azimut, length)])
        # Note: Check for valid Polygon is too Expensive
        test = polygons
        test.append(poly)
        # if MultiPolygon(test).is_valid:
        polygons.append(poly)
    try:
        un = unary_union(polygons)
    except ValueError as e:
        # Discard Shadow-Polygon
        un = None

    return un


def insert_shadow_polygons(grid_id):
    azimut, elevation = get_grid_info(grid_id)

    polygons = []
    for bldg in get_buildings():
        poly = building_shadow(bldg, azimut, elevation)
        if poly:
            if poly.is_valid:
                poly_str = ';'.join(str(c[0]) + ',' + str(c[1]) for c in list(poly.exterior.coords))
                polygons.append((grid_id, poly_str))
        else:
            # print 'One Shadow-Polygon discarded at Date_ID: ' + str(grid_id)
            pass

    commit_many('INSERT INTO Shadow(GridID, Polygon) VALUES (?, ?)', polygons)
    # print 'Completion of Grid_ID: ' + str(grid_id)
    return
