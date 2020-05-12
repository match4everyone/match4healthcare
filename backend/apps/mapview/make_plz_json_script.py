""" # noqa: D2,D400
import pgeocode
import json
from os.path import dirname, abspath, join
from math import radians, sin, cos, asin, sqrt
import csv

plzs = {}

current_location = dirname(abspath(__file__))
from os.path import join

for countrycode in ["DE", "AT"]:
    with open(join(current_location, f'files/{countrycode}.csv'), encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        plzs[countrycode] = {}
        for row in reader:
            for plz in row["plz"].split(","):
                try:
                    if plz not in plzs[countrycode]:
                        plzs[countrycode][plz] = (float(row["lon"]), float(row["lat"]), row["ort"])
                except Exception as e:
                    print("Warning: count not make PLZ entry for", row)
    df = pgeocode.Nominatim(countrycode)._data_frame.dropna()[["postal_code", "longitude", "latitude", "place_name"]].values
    for plz, lon, lat, ort in df:
        if plz not in plzs[countrycode]:
            plzs[countrycode][plz] = (lon, lat, ort)



with open(join(current_location, "files/plzs_merged.json"), "w") as f:
    f.write(json.dumps(plzs))
"""
