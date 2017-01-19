from database import query_db
import matplotlib.pyplot as plt

def run_analysis():
    data = query_db('SELECT MIN(Elevation), MAX(Elevation), MIN(Azimut), MAX(Azimut) FROM Date')[0]

    min_elev = data[0]
    max_elev = data[1]
    min_azimut = data[2]
    max_azimut = data[3]

    print 'Min Elevation: ' + str(min_elev)
    print 'Max Elevation: ' + str(max_elev)
    print 'Min Azimut: ' + str(min_azimut)
    print 'Max Azimut: ' + str(max_azimut)
    return


'''
Min Elevation: 0.0
Max Elevation: 65.0790406657
Min Azimut: 61.0506492828
Max Azimut: 298.4230877
'''


def plot_grid():
    grid = query_db('SELECT Azimut, Elevation FROM Grid')
    x = []
    y = []
    for row in grid:
        x.append(row[0])
        y.append(row[1])

    plt.plot(x, y, 'ro')
    plt.axis('equal')
    plt.show()
    return


def plot_dates():
    grid = query_db('SELECT Azimut, Elevation FROM Date')
    x = []
    y = []
    for row in grid:
        x.append(row[0])
        y.append(row[1])
    plt.plot(x, y, 'ro')
    plt.axis('equal')
    plt.show()
    return


'''
for p in polygons:
    x, y = p.exterior.xy
    fig = plt.figure(1, figsize=(5, 5), dpi=90)
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    ax.set_title('Polygon Edges')
plt.show()
'''