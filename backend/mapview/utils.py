import csv
from math import radians, sin, cos, asin, sqrt




plzs = {}


for countrycode in ["DE", "AT"]:
    with open("mapview/"+ countrycode + ".csv", encoding='utf-8') as csvfile:
      reader = csv.DictReader(csvfile)
      plzs[countrycode] = {}
      for row in reader:
          try:
              plzs[str(countrycode)][row["plz"]] = (float(row["lon"]), float(row["lat"]), row["ort"])
          except:
              pass
              #print("Warning: count not make PLZ entry for", row)



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
