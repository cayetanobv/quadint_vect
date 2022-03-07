import numpy as np


B = np.array([
    0x5555555555555555,
    0x3333333333333333,
    0x0F0F0F0F0F0F0F0F,
    0x00FF00FF00FF00FF,
    0x0000FFFF0000FFFF
])
S = np.array([1, 2, 4, 8, 16])

MAX_ZOOM = 31

MAX_LONGITUDE = 180.0
MAX_LATITUDE = 85.05112877980659  # (2*atan(exp(M_PI))*180.0/M_PI - 90.0)
MIN_LONGITUDE = -MAX_LONGITUDE
MIN_LATITUDE = -MAX_LATITUDE

WEBMERCATOR_R = 6378137.0

XY_SCALE = 2147483648.0  # (double)((uint32)1 << MAX_ZOOM)
INV_XY_SCALE = (1.0 / XY_SCALE)
WM_RANGE = (2.0 * np.pi * WEBMERCATOR_R)
INV_WM_RANGE = (1.0 / WM_RANGE)
WM_MAX = (np.pi * WEBMERCATOR_R)


def xy2quadint(x, y):
    x = (x | (x << S[4])) & B[4]
    y = (y | (y << S[4])) & B[4]

    x = (x | (x << S[3])) & B[3]
    y = (y | (y << S[3])) & B[3]

    x = (x | (x << S[2])) & B[2]
    y = (y | (y << S[2])) & B[2]

    x = (x | (x << S[1])) & B[1]
    y = (y | (y << S[1])) & B[1]

    x = (x | (x << S[0])) & B[0]
    y = (y | (y << S[0])) & B[0]

    return x | (y << 1)


def lonlat2xy(lons, lats, zoom):
    lons = np.minimum(MAX_LONGITUDE, np.maximum(MIN_LONGITUDE, lons))
    lats = np.minimum(MAX_LATITUDE, np.maximum(MIN_LATITUDE, lats))

    fx = (lons + 180.0) / 360.0
    sinlat = np.sin(lats * np.pi / 180.0)
    fy = 0.5 - np.log((1 + sinlat) / (1 - sinlat)) / (4 * np.pi)

    mapsize = 1 << min(MAX_ZOOM, zoom)

    x = np.floor(fx * mapsize).astype(np.int64)
    y = np.floor(fy * mapsize).astype(np.int64)
    x = np.minimum(mapsize - 1, np.maximum(0, x)).astype(np.int64)
    y = np.minimum(mapsize - 1, np.maximum(0, y)).astype(np.int64)

    return x, y


def lonlat2quadint(lons, lats, zoom):
    x, y = lonlat2xy(lons, lats, zoom)
    return xy2quadint(x, y)


def webmercator2xy(wm_x, wm_y):
    x = (wm_x * INV_WM_RANGE + 0.5) * XY_SCALE
    y = (0.5 - wm_y * INV_WM_RANGE) * XY_SCALE

    return x, y


def webmercatorzoom2xy(wm_x, wm_y, zoom):
    XY_SCALE = 1 << zoom

    x = (wm_x * INV_WM_RANGE + 0.5) * XY_SCALE
    y = (0.5 - wm_y * INV_WM_RANGE) * XY_SCALE

    return x, y
