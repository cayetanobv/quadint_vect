import numpy as np
import quadint_vect
import quadkey


def test_comparing_with_orig_library():
    lons = np.array([-6., -2., 2.])
    lats = np.array([37., 40., 39.])

    zoom = 31

    x, y = quadint_vect.lonlat2xy(lons, lats, zoom)
    quadint = quadint_vect.xy2quadint(x, y)
    quadint2 = quadint_vect.lonlat2quadint(lons, lats, zoom)

    print(x, y)
    print(quadint)
    print(quadint2)

    print('\n--python-quadkey version')
    for _lat, _lon in zip(lons, lats):
        _x, _y = quadkey.lonlat2xy(_lat, _lon)
        _quadint = quadkey.xy2quadint(_x, _y)
        _quadint2 = quadkey.lonlat2quadint(_lat, _lon)
        print(_x, _y, _quadint, _quadint2)


def test_large_array():
    prec = 0.1
    sz = 1000
    lat_max, lon_max, lat_min, lon_min = 50., -100., 20., 100.
    lat = np.linspace(lat_max, lat_min, num=int((180. * prec) + 1))
    lon = np.linspace(lon_min, lon_max, num=int((360. * prec) + 1))

    lons, lats = np.random.choice(lat, sz), np.random.choice(lon, sz)

    zoom = 31

    quadint = quadint_vect.lonlat2quadint(lons, lats, zoom)

    print(quadint)


if __name__ == '__main__':
    print('\nTest: test_comparing_with_orig_library')
    test_comparing_with_orig_library()

    print('\nTest: test_large_array')
    test_large_array()
