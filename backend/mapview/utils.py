import csv
plzs = {}
with open("mapview/PLZ.tab", encoding='utf-8') as tsvfile:
  reader = csv.DictReader(tsvfile, dialect='excel-tab')
  for row in reader:
      plzs[row["plz"]] = (float(row["lon"]), float(row["lat"]), row["Ort"])

from math import radians, sin, cos, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * 6371 * asin(sqrt(a))


def get_plzs_close_to(plz, distance_in_km):

    lon1, lat1, _ = plzs[plz]

    close = []
    for other_plz, (lon2, lat2, ort) in plzs.items():
        dist = haversine(lon1, lat1, lon2, lat2)
        if dist < distance_in_km:
            close.append(other_plz)

    return close
