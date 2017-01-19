from shapely import speedups
from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np
from config import bounds
from database import commit_db, get_buildings, get_grid_info

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

    if elevation == 0.:
        top_l = str(bounds['north']) + ',' + str(bounds['west'])
        top_r = str(bounds['north']) + ',' + str(bounds['east'])
        bot_r = str(bounds['south']) + ',' + str(bounds['east'])
        bot_l = str(bounds['south']) + ',' + str(bounds['west'])
        polygon = [top_l, top_r, bot_r, bot_l, top_l]
        commit_db('INSERT INTO Shadow(GridID, Polygon) VALUES (?, ?)', [grid_id, ';'.join(polygon)])
    else:
        polygons = []
        for bldg in get_buildings():
            poly = building_shadow(bldg, azimut, elevation)
            if poly:
                if poly.is_valid:
                    polygons.append(building_shadow(bldg, azimut, elevation))
            else:
                # print 'One Shadow-Polygon discarded at Date_ID: ' + str(grid_id)
                pass

        try:
            union = unary_union(polygons)
            shadow_polys = []
            if union.geom_type == 'Polygon':
                print '1'
                shadow_polys = [list(union.exterior.coords)]
            elif union.geom_type == 'MultiPolygon':
                for p in union:
                    shadow_polys.append(list(p.exterior.coords))

            for p in shadow_polys:
                coords = []
                for c in p:
                    coords.append(','.join([str(c[0]), str(c[1])]))
                commit_db('INSERT INTO Shadow(GridID, Polygon) VALUES (?, ?)', [grid_id, ';'.join(coords)])

            # print 'Completion of Grid_ID: ' + str(grid_id)
        except ValueError as e:
            # print '-'*10+'Unknown Error at Building Shadow Polygons for Date_ID: ' + str(grid_id) + '-'*10
            # print e.message
            '''
            for p in polygons:
                x, y = p.exterior.xy
                fig = plt.figure(1, figsize=(5, 5), dpi=90)
                ax = fig.add_subplot(111)
                ax.plot(x, y)
                ax.set_title('Polygon Edges')
            plt.show()
            '''
    return
