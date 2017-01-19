import sqlite3
from config import database
import os


def commit_db(sql, args=()):
    if not os.path.exists(database):
        connection = sqlite3.connect(database)
        connection.close()
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(sql, args)
    connection.commit()
    connection.close()
    return


def query_db(query, args=()):
    connection = sqlite3.connect(database)
    cur = connection.cursor().execute(query, args)
    return cur.fetchall()


def commit_many(sql, data):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.executemany(sql, data)
    connection.commit()
    connection.close()
    return


def new_table(entity):
    if entity == 'Nodes':
        commit_db('DROP TABLE IF EXISTS Nodes')
        commit_db('CREATE TABLE Nodes('
                  'NodeID INTEGER PRIMARY KEY,'
                  'Lat FLOAT,'
                  'Lon FLOAT)')
    elif entity == 'Weighted':
        commit_db('DROP TABLE IF EXISTS Weighted')
        commit_db('CREATE TABLE Weighted('
                  'GridID INTEGER,'
                  'GraphID INTEGER,'
                  'Factor FLOAT);')
    elif entity == 'Bounds':
        commit_db('DROP TABLE IF EXISTS Bounds')
        commit_db('CREATE TABLE Bounds('
                  'Direction TEXT,'
                  'Value FLOAT);')
    elif entity == 'BoundsBuildings':
        commit_db('DROP TABLE IF EXISTS BoundsBuildings')
        commit_db('CREATE TABLE BoundsBuildings('
                  'Polygon TEXT);')
    elif entity == 'Buildings':
        commit_db('DROP TABLE IF EXISTS Buildings')
        commit_db('CREATE TABLE Buildings('
                  'Polygon TEXT,'
                  'Height FLOAT,'
                  'HeightGround FLOAT);')
    elif entity == 'Shadow':
        commit_db('DROP TABLE IF EXISTS Shadow')
        commit_db('CREATE TABLE Shadow('
                  'GridID INTEGER,'
                  'Polygon TEXT);')
    elif entity == 'Graph':
        commit_db('DROP TABLE IF EXISTS Graph')
        commit_db('CREATE TABLE Graph('
                  'GraphID INTEGER PRIMARY KEY,'
                  'FromID INTEGER,'
                  'ToID INTEGER,'
                  'Costs FLOAT);')
    elif entity == 'Grid':
        commit_db('DROP TABLE IF EXISTS Grid')
        commit_db('CREATE TABLE Grid('
                  'GridID INTEGER PRIMARY KEY,'
                  'Azimut FLOAT,'
                  'Elevation FLOAT);')
    elif entity == 'Date':
        commit_db('DROP TABLE IF EXISTS Date')
        commit_db('CREATE TABLE Date('
                  'DateID INTEGER PRIMARY KEY,'
                  'GridID INTEGER,'
                  'Day INTEGER,'
                  'Hour INTEGER,'
                  'Minute INTEGER,'
                  'Azimut FLOAT,'
                  'Elevation FLOAT);')
    return


def get_buildings():
    return query_db('SELECT * FROM Buildings')


def get_grid_info(grid_id):
    return query_db('SELECT Azimut, Elevation FROM Grid WHERE gridID = ?', [grid_id])[0]


def get_polygons(grid_id):
    polygons = []
    for row in query_db('SELECT Polygon FROM Shadow WHERE GridID = ?', [grid_id]):
        polygons.append([(float(coordinate.split(',')[0]), float(coordinate.split(',')[1])) for coordinate in row[0].split(';')])
    return polygons


def get_graph():
    nodes = {}
    for row in query_db('SELECT * FROM Nodes'):
        nodes[row[0]] = (row[1], row[2])
    return query_db('SELECT * FROM Graph'), nodes


def get_bounds_buildings():
    poly = query_db('SELECT Polygon FROM BoundsBuildings')[0][0]
    return [(float(coordinate.split(',')[0]), float(coordinate.split(',')[1])) for coordinate in poly.split(';')]
