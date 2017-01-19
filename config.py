database = 'database.db'

bounds = {
    'west': 10.877044240271672,
    'east': 10.915640681173187,
    'north': 48.381499267422946,
    'south': 48.35354955784755
}

osm_url = 'http://overpass-api.de/api/map?bbox=' \
           + str(bounds['west']) + ',' \
           + str(bounds['south']) + ',' \
           + str(bounds['east']) + ',' \
           + str(bounds['north'])
