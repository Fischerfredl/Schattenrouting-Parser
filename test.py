import numpy as np
import matplotlib.pylab as plt
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union
from shapely import speedups

speedups.enable()


p1 = Polygon([(1., 1.), (1., 7.), (6., 7.), (2., 6.), (2., 2.), (6., 1.)])
p2 = Polygon([(8., 7.), (8., 1.), (3., 1.), (7., 2.), (7., 6.), (3., 7.)])


fig = plt.figure(1, figsize=(5, 5), dpi=90)
ax = fig.add_subplot(111)

p3 = unary_union([p1, p2])

line = LineString([(0., 0.), (9., 9.)])

intersect = line.intersection(p3)
print intersect

for l in intersect:
    x, y = l.xy
    print ax.plot(x, y)

print p3

x, y = p3.exterior.xy
ax.plot(x, y)
for interior in p3.interiors:
    x, y = interior.xy
    ax.plot(x, y)

plt.show()


