import os
import sqlite3


def entry_database(path, nodes, edges):
    # Loesche Tabelle --------------------------------------------------------------------------------------------------
    if os.path.exists(path):
        print 'Datenbank gefunden. Tabellen <Nodes>, <Edges> werden geloescht'
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        sql = 'DROP TABLE IF EXISTS Nodes'
        cursor.execute(sql)
        connection.commit()
        sql = 'DROP TABLE IF EXISTS Edges'
        cursor.execute(sql)
        connection.commit()
        connection.close()

    # Erstelle neue Datenbank ------------------------------------------------------------------------------------------
    print 'Tabellen <Nodes>, <Edges> wird neu angelegt'
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    sql = 'CREATE TABLE Nodes(' \
          'NodeID TEXT PRIMARY KEY,' \
          'Lat FLOAT,' \
          'Lon FLOAT);'
    cursor.execute(sql)
    connection.commit()
    sql = 'CREATE TABLE Edges(' \
          'Start TEXT,' \
          'Ende TEXT,' \
          'Kosten FLOAT);'
    cursor.execute(sql)
    connection.commit()
    connection.close()

    # Fuelle Nodes -----------------------------------------------------------------------------------------------------
    print 'Lege Datenbankeintraege fuer <Nodes> an'
    # Bereite Daten vor
    node_array = []
    for node in nodes:
        node_array.append((node, nodes[node][0], nodes[node][1]))

    # Fuege Daten in Datenbank ein
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    sql = "INSERT INTO Nodes(NodeID, Lat, Lon) VALUES (?, ?, ?)"
    try:
        cursor.executemany(sql, node_array)
        connection.commit()
    except sqlite3.Error as er:
        print 'SQL Error: ' + er.message

    connection.close()

    # Fuelle Edges -----------------------------------------------------------------------------------------------------
    print 'Lege Datenbankeintraege fuer <Edges> an'
    # Bereite Daten vor
    edge_array = []
    for start in edges:
        for end in edges[start]:
            dist = edges[start][end]
            edge_array.append((start, end, dist))

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    sql = "INSERT INTO Edges(Start, Ende, Kosten) VALUES (?, ?, ?)"
    try:
        cursor.executemany(sql, edge_array)
        connection.commit()
    except sqlite3.Error as er:
        print 'SQL Error: ' + er.message
    connection.close()

    return