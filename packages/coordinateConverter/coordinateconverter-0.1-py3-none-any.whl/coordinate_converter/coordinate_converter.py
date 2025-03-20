from pyproj import Transformer

def wgs84_to_lest97(lat, lon):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3301", always_xy=False)
    y, x = transformer.transform(lat, lon)
    return y, x

def lest97_to_wgs84(y, x):
    transformer = Transformer.from_crs("EPSG:3301", "EPSG:4326", always_xy=False)
    lat, lon = transformer.transform(y, x)
    return lat, lon



