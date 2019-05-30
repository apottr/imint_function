import os,json,arrow,boto3
import botocore.vendored.requests as requests
from shapely.geometry import shape
from botocore.exceptions import ClientError


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
    now = arrow.now
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

def grab_img(url,footprint,stamp):
    fname = url.split('/')[-1]
    s3 = boto3.client('s3')
    with open(f"/tmp/{fname}","wb") as f:
        r = requests.get(url)
        f.write(r.content)
    try:
        resp = s3.upload_file(f'/tmp/{fname}', 'collector-storage', f'landsat/{stamp.year}/{stamp.month}/{stamp.day}/{stamp.hour}/{fname}',
                                ExtraArgs={'Metadata': {'footprint': footprint}})
    except ClientError as e:
        print(e)
        return False
    return True

def get_imgs(bbox):
    out = []
    l = login()
    o = query_data(l,bbox)
    for img in o["data"]["results"]:
        footprint = shape(img["spatialFootprint"]).wkt
        timestamp = arrow.get(img["acquisitionDate"],'YYYY-MM-DD')
        url = img["browseUrl"]
        on_s3 = grab_img(url,footprint,timestamp)
        out.append({
            "date": timestamp.format(),
            "footprint": footprint,
            "imgLocation": url,
            "on_s3": on_s3
        })
    return out



if __name__ == "__main__":
    print(get_imgs({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))