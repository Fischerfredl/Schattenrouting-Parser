from solar_position import calculate_times
from database import new_table, commit_many
from progressbar import progress


def parse_date():
    data = []

    for i in xrange(366):
        data.extend(calculate_times(i+1))
        progress(i+1, 366)

    new_table('Date')

    commit_many('INSERT INTO Date(Day, Hour, Minute, Azimut, Elevation) VALUES(?, ?, ?, ?, ?)', data)
    return
