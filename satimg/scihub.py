import requests,os,arrow
from xml.etree import ElementTree as ET

#search scihub over AOI: https://scihub.copernicus.eu/dhus/search?q=footprint:"Intersects(POLYGON((-4.53 29.85,26.75 29.85,26.75 46.80,-4.53 46.80,-4.53 29.85)))"

ns = {"ns1": "http://www.w3.org/2005/Atom"}

def query_opensearch(bbox):
    # {"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }
    # to poly: POLYGON((nw[0],nw[1] se[0],nw[1] se[0],se[1] nw[0],se[1]))
    s = requests.session()
    s.auth = (os.environ["SH_USER"],os.environ["SH_PASS"])
    nw = bbox["nw"]
    se = bbox["se"]
    query = f"POLYGON(({nw[0]} {nw[1]}, {se[0]} {nw[1]}, {se[0]} {se[1]}, {nw[0]} {se[1]}, {nw[0]} {nw[1]}))"
    r = s.get(f'https://scihub.copernicus.eu/dhus/search?q=footprint:"Intersects({query})"')
    return r.text

def parse_object(xml):
    xp = lambda x: xml.find(f"ns1:{x}",ns).text
    try:
        return {
            "date": arrow.get(xp("date[@name='ingestiondate']")).format(),
            "footprint": xp("str[@name='footprint']"),
            "img": xml.find("ns1:link[@rel='icon']",ns).get("href")
        }
    except Exception as e:
        print(ET.tostring(xml))
        raise(e)

def get_imgs(bbox):
    out = []
    d = query_opensearch(bbox)
    root = ET.fromstring(d)
    for row in root.findall("ns1:entry",ns):
        out.append(parse_object(row))
    return out

if __name__ == "__main__":
    print(get_imgs({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))