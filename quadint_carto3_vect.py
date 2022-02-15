import numpy as np


MAX_LONGITUDE = 180.0
MAX_LATITUDE = 85.05112877980659  # (2*atan(exp(M_PI))*180.0/M_PI - 90.0)
MIN_LONGITUDE = -MAX_LONGITUDE
MIN_LATITUDE = -MAX_LATITUDE

MAX_ZOOM = 31


def quadint_from_ZXY(zoom, X, Y):
    """
    Convert tile coordinates to quadint at specific zoom level
    """
    if zoom < 0 or zoom > MAX_ZOOM:
        raise Exception('Wrong zoom')

    # quadint = Y
    # quadint = quadint << zoom
    # quadint = quadint | X
    # quadint = quadint << 5
    # quadint = quadint | zoom
    #
    # return quadint

    # (z & 0x1F) | (x << 5) | (y << (z + 5))
    return (zoom & 0x1F) | (X << 5) | (Y << (zoom + 5))


def point_to_tile_fraction(lons, lats, zoom):
    """
    Get the precise fractional tile location for a point at a zoom level
    """
    sin = np.sin(lats * np.pi / 180.0)
    z2 = zoom**2
    X = z2 * (lons / 360 + 0.5)
    Y = z2 * (0.5 - 0.25 * np.log((1 + sin) / (1 - sin)) / np.pi)

    # Wrap Tile X
    X = X % z2
    X[X < 0] += z2

    return X, Y


def point_to_tile(lons, lats, zoom):
    """
    Get the tile for a point at a specified zoom level
    """
    X, Y = point_to_tile_fraction(lons, lats, zoom)
    X = np.floor(X).astype(np.int64)
    Y = np.floor(Y).astype(np.int64)

    return X, Y


def quadint_from_location(lons, lats, zoom):
    """
    Get quadint for location at specific zoom level
    """
    if zoom < 0 or zoom > MAX_ZOOM:
        raise Exception('Wrong zoom')

    lons = np.minimum(MAX_LONGITUDE, np.maximum(MIN_LONGITUDE, lons))
    lats = np.minimum(MAX_LATITUDE, np.maximum(MIN_LATITUDE, lats))

    X, Y = point_to_tile(lons, lats, zoom)

    return quadint_from_ZXY(zoom, X, Y)
