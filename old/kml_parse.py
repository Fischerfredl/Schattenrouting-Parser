import xml.etree.ElementTree as ET

from data.progressbar import progress

from kml_coordinates import get_mittelpunkt


# Lese KML-Date und schreibe Daten in die liste gebaeude-------------------------------------------------
# gebaude: Liste der Gebaeude. Jedes Gebaeude wird als Liste Repraesentiert:
#  GEBID, Name, Hoehe Grund, Hoehe Dach, Gebaeude Hoehe, Koordinaten, lon_m, lat_m

def kml_parse(path):
    gebaeude = []

    print 'Lese KML-Datei ein'
    baum = ET.parse(path)  # Lese KML-Datei
    root = baum.getroot()  # Hole Wurzel des Baums

    ns = '{http://www.opengis.net/kml/2.2}'  # XML Namespace

    print 'Start: Durchlaufe alle Gebaeude'
    i = 0
    i_max = len(root.findall('.//'+ns+'Placemark',))
    for placemark in root.findall('.//' + ns + 'Placemark', ):  # Durchlaufe alle Gebaeude
        # Hole die zu dem Gebaeude gehoerenden Variablen
        name = placemark.find(ns + 'name').text

        desc = placemark.find(ns + 'description').text.strip().split('\n')
        gebid = ''
        hoehe_grund = 0.
        hoehe_dach = 0.
        hoehe_geb = 0.
        for item in desc:
            if item.find('GEBID ') == 0:
                gebid = item.rsplit(' ', 1)[1]
            elif item.find('Hoehe Grund:') == 0:
                hoehe_grund = float(item.rsplit(' ', 1)[1])
            elif item.find('Hoehe Dach:') == 0:
                hoehe_dach = float(item.rsplit(' ', 1)[1])
            elif item.find('Gebaeudehoehe') == 0:
                hoehe_geb = float(item.rsplit(' ', 1)[1])

        coords = ''
        coordinates = placemark.find('.//' + ns + 'coordinates').text.strip().split('\n')
        for item in coordinates:
            splitted = item.strip().split(',')
            coords = coords + splitted[1] + ',' + splitted[0] + ';'
        coords = coords[:-1]

        lat_m, lon_m = get_mittelpunkt(coords)

        # Lege Gebaeude an
        geb = [gebid, name, hoehe_grund, hoehe_dach, hoehe_geb, coords, lat_m, lon_m]

        # Haenge das Gebaeude an die Liste an
        gebaeude.append(geb)

        # Fortschritt anzeigen
        i += 1
        progress(i, i_max)
    print 'Ende: Durchlaufe alle Gebaeude\n'
    return gebaeude
