import numpy as np

from external.dijkstra import Dijkstra


# Gibt nodes als dictionary zurueck: Key = ID, Value = (lon, lat)
def get_nodes(root):
    print 'Schreibe Nodes in dictionary'
    nodes = {}
    for nd in root.findall('node'):
        nodes[nd.get('id')] = (float(nd.get('lat')), float(nd.get('lon')))
    return nodes


# Berechnet die distanz zwischen zwei Koordinatenpaaren
def get_dist(coords_start, coords_end):
    lat1 = coords_start[0]
    lon1 = coords_start[1]
    lat2 = coords_end[0]
    lon2 = coords_end[1]
    lat = ((lat1 + lat2)/2)
    dx = 111.3 * np.cos(lat*(np.pi/180)) * (lon1-lon2)
    dy = 111.3 * (lat1-lat2)
    return np.sqrt(dx*dx+dy*dy)


# Fuegt die Nodes aus dem Weg dem Graphen hinzu. Berechnet Nachbarschaften mit Distanz
def way_to_graph(way, nodes, graph):
    nodeids = [nd.get('ref') for nd in way.findall('nd')]
    for i, nd in enumerate(nodeids):
        if i != 0:
            start = nodeids[i-1]
            end = nodeids[i]
            dist = get_dist(nodes.get(start), nodes.get(end))

            if graph.get(start) is None:
                graph[start] = {end: dist}
            else:
                graph[start][end] = dist

            if graph.get(end) is None:
                graph[end] = {start: dist}
            else:
                graph[end][start] = dist
    return


# Gibt hoechste zusammenhaengende Komponente des OSM-Datasource als Graph aus
def get_graph(root):
    nodes = get_nodes(root)

    # Initialisiere Graph
    graph = {}
    print 'Erzeuge Graph'
    for way in root.findall('way'):
        way_to_graph(way, nodes, graph)

    # Suche groessten Spannbaum. Entferne Nodes von kleinen Spannbaeumen aus {Nodes}
    largest = {}
    remaining_nodes = graph.keys()
    print 'Start: Suche groessten Spannbaum'
    i = 1
    while remaining_nodes:
        connected = Dijkstra(graph, remaining_nodes[0])[0]
        if len(connected) > len(largest):
            for key in largest.keys():
                nodes.pop(key)
            largest = connected
        else:
            for key in connected.keys():
                nodes.pop(key)
        for key in connected.keys():
            remaining_nodes.remove(key)
        i += 1
    print 'Ende: Suche groessten Spannbaum. Groesse: ' + str(len(largest)) + ' Nodes von ' + str(len(graph)) + ' Nodes'

    # Zurueckgeben von Nodes (Koordinaten) und Edges (Eigentlicher Graph)
    edges = {}
    for key in largest.keys():
        edges[key] = graph[key]

    return nodes, edges
