import requests,os,json,arrow
from arrow import now
from shapely.geometry import shape


root = "https://earthexplorer.usgs.gov/inventory/json/v/1.4.0"

def makeApiReq(endpoint,data):
    r = requests.post(f"{root}/{endpoint}",params="jsonRequest="+json.dumps(data))
    return r.json()

def login():
    d = makeApiReq("login",{
        "username": os.environ["LS_USER"],
        "password": os.environ["LS_PASS"],
        "authType": "EROS",
        "catalogId": "EE",
        "applicationContext": "INVSC"
    })
    return d

def query_data(login_obj,bbox):
    apikey = login_obj["data"]
    nw,se = bbox["nw"],bbox["se"]
    data = {
        "datasetName": "LSR_LANDSAT_8_C1",
        "spatialFilter": {
            "filterType": "mbr",
            "lowerLeft": {
                "latitude": se[1],
                "longitude": nw[0]
            },
            "upperRight": {
                "latitude": nw[1],
                "longitude": se[0] 
            }
        },
        "temporalFilter": {
            "dateField": "search_date",
            "startDate": now().shift(months=-1).isoformat(),
            "endDate": now().isoformat()
        },
        "maxResults": 10,
        "startingNumber": 1,
        "sortOrder": "ASC",
        "apiKey": apikey
    }
    return makeApiReq("search",data)

def get_imgs(bbox):
    out = []
    l = login()
    o = query_data(l,bbox)
    for img in o["data"]["results"]:
        out.append({
            "date": arrow.get(img["acquisitionDate"],'YYYY-MM-DD').format(),
            "footprint": shape(img["spatialFootprint"]).wkt,
            "img": img["browseUrl"]
        })
    return out



if __name__ == "__main__":
    print(get_imgs({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))