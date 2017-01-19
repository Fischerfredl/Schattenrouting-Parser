import os
import sqlite3

# GEBID, Name, Hoehe Grund, Hoehe Dach, Gebaeude Hoehe, Koordinaten
# Schreibe die Liste 'gebaeude' in die Datenbank------------------------------------------------------------------------


def kml_entry_database(path, gebaeude):
    # Loesche Tabelle
    if os.path.exists(path):
        print 'Datenbank gefunden. Tabelle <Gebaeude> Wird geloescht'
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        sql = 'DROP TABLE IF EXISTS "Gebaeude"'
        cursor.execute(sql)
        connection.commit()
        connection.close()

    # Erstelle neue Tabelle
    print 'Tabelle <Gebaeude> wird neu angelegt'
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    sql = 'CREATE TABLE Gebaeude(' \
          'GebID TEXT PRIMARY KEY,' \
          'Name TEXT,' \
          'HoeheGrund FLOAT,' \
          'HoeheDach FLOAT,' \
          'Gebaeudehoehe FLOAT,' \
          'Koordinaten TEXT,' \
          'Lat_m FLOAT,' \
          'Lon_m FLOAT);'
    cursor.execute(sql)
    connection.commit()
    connection.close()

    # Fuelle Tabelle
    print 'Lege Datenbankeintraege fuer <Gebaeude> an'
    connection = sqlite3.connect(path)
    cursor = connection.cursor()

    sql = "INSERT INTO Gebaeude(GebID, Name, HoeheGrund, HoeheDach, Gebaeudehoehe, Koordinaten, Lat_m, Lon_m) " \
          "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    try:
        cursor.executemany(sql, gebaeude)
        connection.commit()
    except sqlite3.Error as er:
            print 'SQL Error: ' + er.message
    connection.close()
    return


def get_bounds(path):
    bounds = {}
    connection = sqlite3.connect(path)
    cur = connection.cursor().execute('SELECT MAX(Lat_m), MIN(Lat_m), MIN(Lon_m), MAX(Lon_m) FROM Gebaeude').fetchall()
    north, south, west, east = cur[0]
    bounds['north'] = north + 0.002
    bounds['south'] = south - 0.002
    bounds['east'] = east + 0.006
    bounds['west'] = west - 0.003
    return bounds
