import numpy as np
import quadint_vect
import quadint_carto3_vect
import quadkey


def test_comparing_with_orig_library():
    lons = np.array([-3.7038, -6., -2., 2.])
    lats = np.array([40.4168, 37., 40., 39.])

    zoom = 31

    X, Y = quadint_vect.lonlat2xy(lons, lats, zoom)
    quadint = quadint_vect.xy2quadint(X, Y)
    quadint2 = quadint_vect.lonlat2quadint(lons, lats, zoom)

    print(X, Y)
    print(quadint)
    print(quadint2)

    X_c3, Y_c3 = quadint_carto3_vect.point_to_tile(lons, lats, zoom)
    quadint_c3 = quadint_carto3_vect.quadint_from_ZXY(zoom, X_c3, Y_c3)
    quadint2_c3 = quadint_carto3_vect.quadint_from_location(lons, lats, zoom)

    print(X_c3, Y_c3)
    print(quadint_c3)
    print(quadint2_c3)

    print('\n--python-quadkey version')
    for _lat, _lon in zip(lons, lats):
        _x, _y = quadkey.lonlat2xy(_lon, _lat)
        _quadint = quadkey.xy2quadint(_x, _y)
        _quadint2 = quadkey.lonlat2quadint(_lon, _lat)
        print(_x, _y, _quadint, _quadint2)


def test_large_array():
    prec = 0.1
    sz = 100
    lat_max, lon_max, lat_min, lon_min = 50., -100., 20., 100.
    lat = np.linspace(lat_max, lat_min, num=int((180. * prec) + 1))
    lon = np.linspace(lon_min, lon_max, num=int((360. * prec) + 1))

    lons, lats = np.random.choice(lat, sz), np.random.choice(lon, sz)

    zoom = 31

    quadint = quadint_vect.lonlat2quadint(lons, lats, zoom)
    quadint_c3 = quadint_carto3_vect.quadint_from_location(lons, lats, zoom)

    print(quadint)
    # print(quadint_c3)
    # print(lons, lats)


if __name__ == '__main__':
    print('\nTest: test_comparing_with_orig_library')
    test_comparing_with_orig_library()

    print('\nTest: test_large_array')
    test_large_array()
