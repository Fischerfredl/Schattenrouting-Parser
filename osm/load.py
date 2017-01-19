import urllib2
import xml.etree.ElementTree as ET

from config import osm_url
from progressbar import progress


# ----------------------------------------------------------------------------------------------------------------------
# Tags: read and interpret
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


def load():
    # Fetch data from online api
    print 'Hole OSM daten aus dem Internet. Path: ' + osm_url
    data = urllib2.urlopen(osm_url).read()
    osmroot = ET.fromstring(data)

    # Create XML-Scheme for relevant data
    print 'Lege XML-Struktur an'
    xml = '<osm version="0.6" generator="Filter by Alfred Melch">' \
          '<note>This document contains only ways and nodes considered for passenger routing. ' \
          'It was generated as part of a Bachelor Thesis with the title ' \
          '"Schattenrouting" (Shoadow-Routing) by Alfred Melch</note>' \
          '</osm>'
    root = ET.fromstring(xml)
    root.append(osmroot.find('bounds'))

    # Copy relevant data
    print 'Verarbeite OSM-Datasource'
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
