from arrow import now
from urllib.parse import urlencode
import requests,re

satmap = {
    "DM2": "URTHECAST",
    "EB": "eros",
    "FS2": "formosat",
    "GF1": "gaofen1",
    "GF2": "gaofen2",
    "GE1": "digitalglobe",
    "IK": "ikonos",
    "K2": "kompsat",
    "K3": "kompsat",
    "K3A": "kompsat",
    "P1": "pleiades",
    "QB": "digitalglobe",
    "SP6": "spot6",
    "SKY": "scene",
    "SUPER": "scene",
    "TeL": "scene",
    "ALOS": "alos",
    "TS": "triplesat",
    "WV1": "digitalglobe",
    "WV2": "digitalglobe",
    "WV3": "digitalglobe",
    "WV4": "digitalglobe"
}

def make_bbox(bounds):
    #two sets: {"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }
    #four sets: [[-71.30126953125,42.53486817758702],[-70.7958984375,42.53486817758702],[-70.7958984375,42.204107493733176],[-71.30126953125,42.204107493733176]]
    #four to two: {"nw": four[0], "se": four[2]}
    #two to four: [[nw[0],nw[1]],[se[0],nw[1]],[se[0],se[1]],[nw[0],se[1]]]
    nw = bounds["nw"]
    se = bounds["se"]
    return [[nw[0],nw[1]],[se[0],nw[1]],[se[0],se[1]],[nw[0],se[1]]]

def make_search(bounds):
    bbox = make_bbox(bounds)
    params = {
       "cloudcover_max": 100,
       "offnadir_max": 100,
       "resolution_min": 0,
       "resolution_max": 2,
       "coords": bbox,
       "seasonal": False,
       "startDate": "1970-01-01",
       "endDate": now().shift(days=1).format("YYYY-MM-DD"),
       "satellites": ["DM2","EB","FS2","GF1","GF2","GE1","IK","K2","K3","K3A","P1","QB","SP6","SKY","SUPER","TeL","TS","WV1","WV2","WV3","WV4","ALOS"]
    }
    r = requests.post("https://imagehunter-api.apollomapping.com/ajax/search",headers={
        "Host": "imagehunter-api.apollomapping.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Accept": "*/*",
        "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://imagehunter.apollomapping.com/",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://imagehunter.apollomapping.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    },data=urlencode(params).replace('+',"").replace("%27","%22"))
    return r.json()

def get_image(obj):
    if obj["preview_url"]:
        return obj["preview_url"]
    else:
        sat = obj["collection_vehicle_short"]
        r = requests.post("https://imagehunter-api.apollomapping.com/ajax/get_preview_image",data={
            "catid": obj["objectid"],
            "satellite": satmap[sat],
            "satelliteShortName": sat
        })
        out = r.json()
        return f"https://imagehunter-api.apollomapping.com{out['path']}"

def make_fmt(t):
    x = t.month
    d = str(t.day)
    y = d[0] if len(d) == 2 else "0"
    z = t.year
    return f'{x}-{y}.-{z}'

def get_first(data):
    out = []
    for d in data["results"]:
        if re.match(make_fmt(now()),d["collection_date"]):
            out.append(d)
    return out[0:10]

def grab_comsatimg(bbox):
    d = make_search(bbox)
    f = get_first(d)
    out = []
    for obj in f:
        nw = [obj["topleft"]["x"],obj["topleft"]["y"]]
        se = [obj["bottomright"]["x"],obj["bottomright"]["y"]]
        out.append({
            "footprint": f"POLYGON(({nw[0]} {nw[1]}, {se[0]} {nw[1]}, {se[0]} {se[1]}, {nw[0]} {se[1]}, {nw[0]} {nw[1]}))",
            "img": get_image(obj)
        })
    return out

if __name__ == "__main__":
    #print(grab_comsatimg({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176]}))
    print(make_search({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176]}))
    