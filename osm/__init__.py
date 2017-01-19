from load import load
from process import process
from write import write


def parse_osm():
    xml = load()
    nodes, edges = process(xml)
    write(nodes, edges)
    return
