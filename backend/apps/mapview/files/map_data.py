import json
from os.path import abspath, dirname, join

current_location = dirname(abspath(__file__))

with open(join(current_location, "../files/plzs_merged.json")) as f:
    plzs = json.loads(f.read())
