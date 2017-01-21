from database import query_db, new_table
from graph_calculation import insert_graph
from multiprocessing import Pool, Value
from progressbar import progress

counter = None
i_max = None


def init(c, i):
    global counter
    global i_max
    counter = c
    i_max = i


def process_entry(grid_id):
    insert_graph(grid_id)

    global counter
    global i_max

    with counter.get_lock():
        counter.value += 1
    progress(counter.value, i_max.value)
    return


def parse_graph():
    if __name__ == 'graph':
        grid_ids = [row[0] for row in query_db('SELECT GridID FROM Grid')]
        new_table('Weighted')

        counter = Value('i', 0)
        i = Value('i', len(grid_ids))
        p = Pool(4, initializer=init, initargs=(counter, i))
        p.map(process_entry, grid_ids)
        p.close()

    return
