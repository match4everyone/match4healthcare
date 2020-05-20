from functools import lru_cache
from math import asin, cos, radians, sin, sqrt
import time

from apps.iamstudent.models import Student
from apps.mapview.files.map_data import plzs


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


@lru_cache(maxsize=1)
def prepare_students(ttl_hash=None):
    # Source: https://stackoverflow.com/questions/31771286/python-in-memory-cache-with-time-to-live
    del ttl_hash  # to emphasize we don't use it and to shut pylint up
    students = Student.objects.filter(user__validated_email=True)
    locations_and_number = {}
    i = 0
    for student in students:
        cc = student.countrycode
        plz = student.plz
        key = cc + "_" + plz

        if key in locations_and_number:
            locations_and_number[cc + "_" + plz]["count"] += 1
        else:
            lat, lon, ort = plzs[cc][plz]
            locations_and_number[key] = {
                "countrycode": cc,
                "plz": plz,
                "count": 1,
                "lat": lat,
                "lon": lon,
                "ort": ort,
                "i": i,
            }
            i += 1
    return locations_and_number


def group_by_zip_code(entities):
    countrycode_plz_details = {}

    for entity in entities:
        countrycode = entity.countrycode
        plz = entity.plz

        if countrycode not in countrycode_plz_details:
            countrycode_plz_details[countrycode] = {}

        country = countrycode_plz_details[countrycode]
        if plz not in country:
            country[plz] = {
                "countrycode": countrycode,
                "plz": plz,
                "count": 0,
                **get_plz_data(countrycode, plz),
            }

        country[plz]["count"] += 1
    return countrycode_plz_details


def get_ttl_hash(seconds=300):
    """Return the same value withing `seconds` time period."""
    return round(time.time() / seconds)
