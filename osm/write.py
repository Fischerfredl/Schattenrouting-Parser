from database import new_table, commit_many, commit_db
from config import bounds


def write(nodes, edges):
    new_table('GraphShortest')
    new_table('Nodes')
    new_table('Bounds')

    # Fuelle Nodes -----------------------------------------------------------------------------------------------------
    print 'Lege Datenbankeintraege fuer <Nodes> an'
    # Bereite Daten vor
    node_array = []
    for node in nodes:
        node_array.append((node, nodes[node][0], nodes[node][1]))

    # Lege Daten an
    commit_many('INSERT INTO Nodes(NodeID, Lat, Lon) VALUES (?, ?, ?)', node_array)

    # Fuelle Edges -----------------------------------------------------------------------------------------------------
    print 'Lege Datenbankeintraege fuer <GraphShortest> an'
    # Bereite Daten vor
    edge_array = []
    for start in edges:
        for end in edges[start]:
            dist = edges[start][end]
            edge_array.append((start, end, dist))

    # Lege Daten an
    commit_many('INSERT INTO GraphShortest(FromID, ToID, Costs) VALUES (?, ?, ?)', edge_array)

    # Store Bounds -----------------------------------------------------------------------------------------------------
    commit_db('INSERT INTO Bounds(Direction, Value) VALUES(?, ?)', ['North', bounds['north']])
    commit_db('INSERT INTO Bounds(Direction, Value) VALUES(?, ?)', ['South', bounds['south']])
    commit_db('INSERT INTO Bounds(Direction, Value) VALUES(?, ?)', ['West', bounds['west']])
    commit_db('INSERT INTO Bounds(Direction, Value) VALUES(?, ?)', ['East', bounds['east']])
    return
