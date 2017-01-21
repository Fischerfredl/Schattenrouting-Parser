from datetime import timedelta
from osm import parse_osm
from kml import  parse_kml
from date import parse_date
from shadow import parse_shadow
from time import sleep
from timeit import default_timer as timer
from analysis import run_analysis, plot_grid, plot_dates
from grid import parse_grid
from graph import parse_graph
from date_grid_calculation import date_grid_calculation


def linebreak():
    print '\n' + '-' * 100 + '\n'
    sleep(1)
    return


def osm():
    print 'Start: Parsing of OSM-Data'
    start = timer()
    parse_osm()
    end = timer()
    print 'Tables <GraphShortest> and <Nodes> added'
    print 'End: Parsing of OSM-Data. Took %s hours' % str(timedelta(seconds=end-start))
    return


def kml():
    print 'Start: Parsing of KML-Data'
    start = timer()
    parse_kml()
    end = timer()
    print 'Table <Buildings> added'
    print 'End: Parsing of KML-Data. Took %s hours' % str(timedelta(seconds=end-start))
    return


def date():
    print 'Start: Calculation of Dates'
    start = timer()
    parse_date()
    end = timer()
    print 'Table <Date> added'
    print 'End: Calculating Dates. Took %s hours' % str(timedelta(seconds=end-start))
    return


def grid(steps):
    print 'Start: Calculation of Grid'
    start = timer()
    parse_grid(grid_steps=steps)
    end = timer()
    print 'Table <Grid> added.'
    print 'End: Calculating Grid. Took %s hours' % str(timedelta(seconds=end-start))
    return


def shadow():
    print 'Start: Calculation of Shadow-Polygons'
    start = timer()
    parse_shadow()
    end = timer()
    print 'Tables <Shadow> added'
    print 'End: Calculating Shadow-Polygons. Took %s hours' % str(timedelta(seconds=end-start))
    return


def graph():
    print 'Start: Calculation of Graphs'
    start = timer()
    parse_graph()
    end = timer()
    print 'Tables <Graph> added'
    print 'End: Calculating Graphs. Took %s hours' % str(timedelta(seconds=end-start))
    return


def calc_date_grid():
    print 'Start: Correction of Grid'
    start = timer()
    date_grid_calculation()
    end = timer()
    print 'Tables <Grid> and <Dates> updated'
    print 'End: Correction of Grid. Took %s hours' % str(timedelta(seconds=end - start))
    return

if __name__ == '__main__':

    linebreak()
    osm()
    linebreak()
    kml()
    linebreak()
    date()
    linebreak()
    grid(12)
    linebreak()
    shadow()
    linebreak()
    calc_date_grid()
    linebreak()
    graph()
    linebreak()

    # run_analysis()
    # plot_grid()
    # plot_dates()