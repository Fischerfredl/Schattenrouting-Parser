import numpy as np
import matplotlib.pylab as plt
from shapely.geometry import MultiPolygon, LineString, Polygon
from shapely.ops import unary_union
from shapely import speedups
from database import get_polygons

speedups.enable()


p = MultiPolygon(get_polygons(1))

# p = [Polygon([(3., 1.), (3., 4.), (5., 4.), (5., 1.)]), Polygon([(7., 3.), (7., 6.), (9., 6.), (9., 3.)])]

l = LineString([(1, 1), (10, 5)])
intersec = l.intersection(p)

print l.length
print intersec.length

fig = plt.figure(1, figsize=(5, 5), dpi=90)
ax = fig.add_subplot(111)

for poly in p:
    x, y = poly.exterior.xy
    ax.plot(x, y)

x, y = l.xy
ax.plot(x, y)

plt.show()
