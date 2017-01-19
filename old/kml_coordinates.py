def coords_to_array(coords):
    coord_array = []
    for c in coords.strip().split(';'):
        x, y = c.split(',')
        coord_array.append((float(x), float(y)))
    return coord_array


def get_mittelpunkt(coords):
    coord_array = coords_to_array(coords)
    coord_array.append(coord_array[0])

    # Flaecheninhalt berechnen
    a = 0.
    i = 0
    while i < len(coord_array)-1:
        a += 0.5 * (coord_array[i][0] * coord_array[i+1][1] - coord_array[i+1][0] * coord_array[i][1])
        i += 1

    # x Koordinate des Mittelpunkts berechnen
    x_m = 0.
    i = 0
    while i < len(coord_array) - 1:
        x_m += 1/(6*a) * (coord_array[i][0] + coord_array[i + 1][0]) * \
              (coord_array[i][0] * coord_array[i+1][1] - coord_array[i+1][0] * coord_array[i][1])
        i += 1

    # y Koordinate des Mittelpunkts berechnen
    y_m = 0.
    i = 0
    while i < len(coord_array) - 1:
        y_m += 1/(6*a) * (coord_array[i][1] + coord_array[i + 1][1]) * \
              (coord_array[i][0] * coord_array[i+1][1] - coord_array[i+1][0] * coord_array[i][1])
        i += 1

    return x_m, y_m
