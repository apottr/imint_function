import requests,json,arrow
from shapely.geometry import shape

def make_geojson(bbox):
    return json.dumps({ "type": "Polygon", "coordinates": [[
            bbox["nw"],
            [bbox["se"][0],bbox["nw"][1]],
            bbox["se"],
            [bbox["nw"][0],bbox["se"][1]],
            bbox["nw"]]]})

def query_data(bbox):
    url = "https://sat-api.developmentseed.org/search/stac"
    r = requests.get(url,params={
        "collection": "landsat-8",
        "limit": "10",
        "datetime": "2018-10",
        "intersects": make_geojson(bbox)
    })
    return r.json()

if __name__ == "__main__":
    print(query_data({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))

