from database import query_db, commit_many, new_table


def parse_grid(grid_steps=6.):
    print 'Creating Grid'
    # Erstelle Grid
    min_azimut, max_azimut = query_db('SELECT MIN(Azimut), MAX(Azimut) FROM Date')[0]

    data = []
    while min_azimut <= max_azimut:
        min_elev, max_elev = query_db('SELECT MIN(Elevation), MAX(Elevation) FROM Date WHERE Azimut BETWEEN '
                                      +str(min_azimut-grid_steps/2)+' AND '+str(min_azimut+grid_steps/2))[0]
        while min_elev <= max_elev:
            data.append((min_azimut, min_elev))
            min_elev += grid_steps
        min_azimut += grid_steps

    new_table('Grid')
    commit_many('INSERT INTO Grid(Azimut, Elevation) VALUES (?, ?)', data)
    return
