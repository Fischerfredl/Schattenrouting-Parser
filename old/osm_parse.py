import urllib2
import xml.etree.ElementTree as ET

from data.progressbar import progress


# ----------------------------------------------------------------------------------------------------------------------
# OSM-XML-Tree Erstellen, Formatieren, Schreiben
# ----------------------------------------------------------------------------------------------------------------------

# Liest XMl-Struktur aus Datei ein. Gibt die Wurzel zurueck
def parse_tree(path):
    print 'Lese OSM-File aus ' + path
    osmbaum = ET.parse(path)
    return osmbaum.getroot()


# Holt XML aus Internet
def parse_url(bounds):
    path = 'http://overpass-api.de/api/map?bbox='\
           + str(bounds['west']) + ','\
           + str(bounds['south']) + ','\
           + str(bounds['east']) + ','\
           + str(bounds['north'])
    print 'Hole OSM daten aus dem Internet. Path: '+path
    data = urllib2.urlopen(path).read()
    print 'Werte die Daten aus'
    root = ET.fromstring(data)
    return root


# Schreibt XML-Struktur in Datei
def write_tree(root, path):
    print 'Start: Formatiere und schreibe XML in: ' + path
    root = sort_tree(root)
    indent(root)
    ET.ElementTree(root).write(path, xml_declaration=True, encoding='utf-8', method='xml')
    print "Ende: schreibe in Datei \n"
    return


# Strukturiert die XML-Struktur fuer eine schoene Ausgabe
def indent(elem, level=0):
    i = '\n' + level*'  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    return


# Gebe sortierten Baum zurueck
def sort_tree(elem):
    data = []
    notes = elem.find('note')
    bounds = elem.find('bounds')
    for node in elem.findall('node'):
        nodeid = node.get('id')
        data.append((nodeid, node))
    data.sort()
    nodes = [item[-1] for item in data]
    data = []
    for way in elem.findall('way'):
        wayid = way.get('id')
        data.append((wayid, way))
    data.sort()
    ways = [item[-1] for item in data]
    rootneu = ET.Element(elem.tag)
    rootneu.attrib = elem.attrib
    rootneu.append(notes)
    rootneu.append(bounds)
    for item in nodes:
        rootneu.append(item)
    for item in ways:
        rootneu.append(item)
    return rootneu


# ----------------------------------------------------------------------------------------------------------------------
# Tags: Auslesen und Auswerten
# ----------------------------------------------------------------------------------------------------------------------

def get_tags(elem):
    tags = dict()
    for tag in elem:
        tags[tag.get('k')] = tag.get('v')
    return tags


def way_for_pedestrian_ors(way):
    tags = get_tags(way)
    hw = tags.get('highway')
    sw = tags.get('sidewalk')
    foot = tags.get('foot')
    access = tags.get('access')
    return (
           (hw == 'primary' or hw == 'primary_link' or hw == 'secondary' or hw == 'secondary_link' or
            hw == 'tertiary' or hw == 'tertiary_link' or hw == 'unclassified' or hw == 'residential' or
            hw == 'living_street' or hw == 'track' or hw == 'pedestrian' or
            (hw == 'cycleway' and (foot == 'designated' or foot == 'yes')) or
            (hw == 'service' and (access != 'no' and access != 'private')) or
            hw == 'footway' or hw == 'steps' or hw == 'path')
            and
           (sw != 'none')
           )


def irrelevant_node(node):
    if len(node) == 0:
        return False
    tags = get_tags(node)
    hw = tags.get('highway')
    cr = tags.get('crossing')
    return not (hw == 'crossing' or hw == 'traffic_signals' or (cr != 'no' and cr is not None))


def circular_way(way):
    nodes = way.findall('nd')
    if not nodes:
        return True
    if nodes[0].get('ref') == nodes[-1].get('ref'):
        return True
    return False


# ----------------------------------------------------------------------------------------------------------------------
# Kopieren: Way incl. nodes.
# ----------------------------------------------------------------------------------------------------------------------

def cpy_way_intelligent(way, osmroot, root, nodepositives, nodenegatives):
    root.append(way)
    for nd in way.findall('nd'):
        ref = nd.get('ref')
        if ref in nodepositives:
            pass
        elif ref in nodenegatives:
            way.remove(nd)
        else:
            node = osmroot.find('node[@id="' + ref + '"]')
            if irrelevant_node(node):  # irrelevant node
                way.remove(nd)
                nodenegatives.append(ref)
            else:  # relevant node
                root.append(node)
                nodepositives.append(ref)
    return


# ----------------------------------------------------------------------------------------------------------------------
# Parser fuer die OSM-Verarbeitung
# ----------------------------------------------------------------------------------------------------------------------

def osm_parse(osmroot):
    print 'Verarbeite OSM-Datasource'

    xml = '<osm version="0.6" generator="Filter by Alfred Melch">' \
          '<note>This document contains only ways and nodes considered for passenger routing. ' \
          'It was generated as part of a Bachelor Thesis with the title ' \
          '"Schattenrouting" (Shoadow-Routing) by Alfred Melch</note>' \
          '</osm>'
    root = ET.fromstring(xml)
    root.append(osmroot.find('bounds'))

    i = 0  # Zaehlvariable fuer Fortschrittsberechnung
    i_max = len(osmroot.findall('way'))
    nodepositives = []  # Enthaelt bereits kopierte nodes
    nodenegatives = []  # Enthaelt irrelevante nodes
    print 'Start: Durchsuche alle Wege'
    for way in osmroot.findall('way'):
        if not circular_way(way):
            if way_for_pedestrian_ors(way):
                cpy_way_intelligent(way, osmroot, root, nodepositives, nodenegatives)
        # Fortschritt berechnen
        i += 1
        progress(i, i_max)
    print 'Ende: Durchsuche alle Wege'
    return root
