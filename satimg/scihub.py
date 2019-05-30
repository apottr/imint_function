import os,arrow,boto3
import botocore.vendored.requests as requests
from xml.etree import ElementTree as ET
from botocore.exceptions import ClientError

#search scihub over AOI: https://scihub.copernicus.eu/dhus/search?q=footprint:"Intersects(POLYGON((-4.53 29.85,26.75 29.85,26.75 46.80,-4.53 46.80,-4.53 29.85)))"

ns = {"ns1": "http://www.w3.org/2005/Atom"}

def login():
    s = requests.session()
    s.auth = (os.environ["SH_USER"],os.environ["SH_PASS"])
    return s

def query_opensearch(session,bbox):
    # {"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }
    # to poly: POLYGON((nw[0],nw[1] se[0],nw[1] se[0],se[1] nw[0],se[1]))
    nw = bbox["nw"]
    se = bbox["se"]
    query = f"POLYGON(({nw[0]} {nw[1]}, {se[0]} {nw[1]}, {se[0]} {se[1]}, {nw[0]} {se[1]}, {nw[0]} {nw[1]}))"
    r = session.get(f'https://scihub.copernicus.eu/dhus/search?q=footprint:"Intersects({query})"')
    return r.text

def grab_img(url,footprint,stamp,session):
    fname = url.split('/')[-1]
    s3 = boto3.client('s3')
    with open(f"/tmp/{fname}","wb") as f:
        r = session.get(url)
        f.write(r.content)
    try:
        resp = s3.upload_file(f'/tmp/{fname}', 'collector-storage', f'scihub/{stamp.year}/{stamp.month}/{stamp.day}/{stamp.hour}/{fname}',
                                ExtraArgs={'Metadata': {'footprint': footprint}})
    except ClientError as e:
        print(e)
        return False
    return True
def parse_object(xml,session):
    xp = lambda x: xml.find(f"ns1:{x}",ns).text
    try:
        footprint = xp("str[@name='footprint']")
        timestamp = arrow.get(xp("date[@name='ingestiondate']"))
        url = xml.find("ns1:link[@rel='icon']",ns).get("href")
        on_s3 = grab_img(url,footprint,timestamp,session)
        return {
            "date": timestamp.format(),
            "footprint": footprint,
            "img": url,
            "on_s3": on_s3

        }
    except Exception as e:
        print(ET.tostring(xml))
        raise(e)

def get_imgs(bbox):
    out = []
    s = login()
    d = query_opensearch(s,bbox)
    root = ET.fromstring(d)
    for row in root.findall("ns1:entry",ns):
        out.append(parse_object(row,s))
    return out

if __name__ == "__main__":
    print(get_imgs({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))