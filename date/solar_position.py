import numpy as np
from config import bounds

const = np.pi/180.


def get_decl(t):
    return -23.45 * np.cos(const*360*(t+10)/365.)


def get_zgl(t):
    return 60 * (-0.171*np.sin(0.0337*t+0.465) - 0.1299 * np.sin(0.01787*t-0.168))


def get_stundenwinkel(hour, minute, lon, zgl):
    return 15 * (hour + minute / 60. - (15.-lon)/15. - 12 + zgl/60.)


def get_elev(lat, decl, stundenwinkel):
    x = np.sin(const * lat) * np.sin(const * decl) + \
        np.cos(const * lat) * np.cos(const * decl) * np.cos(const * stundenwinkel)
    return np.arcsin(x) / const


def get_azimut(lat, decl, elev, std):
    y = -(np.sin(const * lat) * np.sin(const * elev) - np.sin(const * decl)) / \
        (np.cos(const * lat) * np.sin(np.arccos(np.sin(const * elev))))
    azimut = np.arccos(y) / const
    return azimut if std >= 0 else 360-azimut


def get_stundenwinkel_diff(elev, lat, decl):
    x = (np.sin(const*elev) - np.sin(const*lat) * np.sin(const*decl)) / (np.cos(const*lat) * np.cos(const*decl))
    stundenwinkel_diff = np.arccos(x) / const
    return stundenwinkel_diff


def get_time(stundenwinkel, lon, zgl):
    time = (12 - stundenwinkel / 180 * 12 - zgl/60.) - lon/15. + 1
    return int(time), int((time-int(time))*60)


def calculate_times(day):
    lat = (bounds['south'] + bounds['north']) / 2
    lon = (bounds['west'] + bounds['east']) / 2

    decl = get_decl(day)
    zgl = get_zgl(day)

    # Sonnenaufgang / -Untergang finden
    elev = 6
    stdw = get_stundenwinkel_diff(elev, lat, decl)
    start_hour, start_minute = get_time(stdw, lon, zgl)
    end_hour, end_minute = get_time(-stdw, lon, zgl)

    array = []
    while start_hour < end_hour or start_minute < end_minute:
        std = -get_stundenwinkel(start_hour, start_minute, lon, zgl)
        elev = get_elev(lat, decl, std)
        azimut = get_azimut(lat, decl, elev, std)
        array.append((day, start_hour, start_minute, azimut, elev))
        start_minute += 1
        if start_minute == 60:
            start_hour += 1
            start_minute = 0

    '''
    # Array initialisieren
    hour, minute = get_time(stdw+6, lon, zgl)
    array = [(day, hour, minute, 180., 0.)]

    # array fuellen
    while elev >= 5.9:
        hour, minute = get_time(stdw, lon, zgl)
        elev = get_elev(lat, decl, stdw)
        azimut = get_azimut(lat, decl, elev, stdw)
        array.append((day, hour, minute, azimut, elev))
        stdw -= 6

    array[-1] = (array[-1][0], array[-1][1], array[-1][2], 180., 0.)
    '''
    return array
