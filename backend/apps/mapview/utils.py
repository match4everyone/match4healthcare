import csv
from os.path import dirname, abspath, join
from math import radians, sin, cos, asin, sqrt
import json

current_location = dirname(abspath(__file__))

with open(join(current_location, "files/plzs_merged.json")) as f:
    plzs = json.loads(f.read())


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


def get_plzs_close_to(countrycode, plz, distance_in_km):
    lon1, lat1, _ = plzs[countrycode][plz]

    close = []
    for other_plz, (lon2, lat2, ort) in plzs[countrycode].items():
        dist = haversine(lon1, lat1, lon2, lat2)
        if dist < distance_in_km:
            close.append(other_plz)

    return close


def get_plz_data(countrycode, plz):
    lat, lon, ort = plzs[countrycode][plz]
    return {"latitude": lat, "longitude": lon, "city": ort}
