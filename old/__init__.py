import os
from time import sleep

from config import config#

from kml_database import kml_entry_database, get_bounds
from old.kml_parse import kml_parse
from osm_database import entry_database
from osm_dijkstra import get_graph
from osm_parse import parse_tree, parse_url, osm_parse, write_tree


def linebreak():
    print '\n' + '-' * 100 + '\n'
    sleep(1)
    return


def parse_to_database():
    if os.path.exists(config['DATABASE']):
        return True
    print 'Start parsing data into database'
    linebreak()

    gebaeude = kml_parse(config['KML_Input'])
    kml_entry_database(config['DATABASE'], gebaeude)
    bounds = get_bounds(config['DATABASE'])
    config['bounds'] = bounds

    linebreak()

    if os.path.exists(config['OSM_OUTPUT']):
        root = parse_tree(config['OSM_OUTPUT'])
    else:
        osmroot = parse_url(bounds)
        root = osm_parse(osmroot)
        write_tree(root, config['OSM_OUTPUT'])

    linebreak()

    g = get_graph(root)

    linebreak()

    entry_database(config['DATABASE'], g[0], g[1])

    linebreak()
    print 'Finished parsing data into database'
    return True
