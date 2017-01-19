import xml.etree.ElementTree as ET
from progressbar import progress
from database import new_table, commit_many


def parse_kml():
    gebaeude = []

    print 'Lese KML-Datei ein\n'
    baum = ET.parse('Augsburg.kml')  # Lese KML-Datei
    root = baum.getroot()  # Hole Wurzel des Baums

    ns = '{http://www.opengis.net/kml/2.2}'  # XML Namespace

    print 'Start: Durchlaufe alle Gebaeude'
    i = 0
    i_max = len(root.findall('.//'+ns+'Placemark',))
    for placemark in root.findall('.//' + ns + 'Placemark', ):  # Durchlaufe alle Gebaeude
        # Hole die zu dem Gebaeude gehoerenden Variablen
        desc = placemark.find(ns + 'description').text.strip().split('\n')
        height_ground = 0.
        height = 0.
        for item in desc:
            if item.find('Hoehe Grund:') == 0:
                height_ground = float(item.rsplit(' ', 1)[1])
            elif item.find('Gebaeudehoehe') == 0:
                height = float(item.rsplit(' ', 1)[1])

        coords = []
        coordinates = placemark.find('.//' + ns + 'coordinates').text.strip().split('\n')
        for item in coordinates:
            splitted = item.strip().split(',')
            coords.append(splitted[1] + ',' + splitted[0])

        polygon = ';'.join(coords)
        # Lege Gebaeude an
        geb = [polygon, height, height_ground]

        # Haenge das Gebaeude an die Liste an
        gebaeude.append(geb)

        # Fortschritt anzeigen
        i += 1
        progress(i, i_max)
    print 'Ende: Durchlaufe alle Gebaeude\n'

    new_table('Buildings')
    print 'Lege Datenbankeintraege fuer <Buildings> an'
    commit_many('INSERT INTO Buildings(Polygon, Height, HeightGround) VALUES (?, ?, ?)', gebaeude)
    return
