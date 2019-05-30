import botocore.vendored.requests as requests
import arrow,boto3
from urllib.parse import urlencode
from botocore.exceptions import ClientError

def pull_data(bbox):
    url = "https://ksatdb.kari.re.kr/arirang/ajax/searchImage.jsp"
    nw,se = bbox["nw"],bbox["se"]
    data = {
        "type": "EASY",
        "geo": f"POLYGON(({nw[0]}+{nw[1]},+{se[0]}+{nw[1]},+{se[0]}+{se[1]},+{nw[0]}+{se[1]},+{nw[0]}+{nw[1]}))",
        "MinCloud":0,
        "MaxCloud":1,
        "period":"~",
        "TiltStart":-60,
        "TiltEnd":60,
        "satNames": "KOMPSAT1,KOMPSAT2,KOMPSAT3,KOMPSAT3A,KOMPSAT5",
        "orderBy": "PRODUCT_CENTERTIME+DESC,CLOUDAVG+ASC,SATNAME+DESC",
        "size":5
    }
    r = requests.post(url,headers={
        "Host": "ksatdb.kari.re.kr",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Accept": "*/*",
        "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://ksatdb.kari.re.kr/arirang/map/map.jsp",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "334",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    },data=urlencode(data).replace("%28","(").replace("%29",")").replace("%2B","+"))
    return r.json()

def grab_image(url,footprint,stamp):
    fname = url.split('/')[-1]
    s3 = boto3.client('s3')
    with open(f"/tmp/{fname}","wb") as f:
        r = requests.get(url)
        f.write(r.content)
    try:
        resp = s3.upload_file(f'/tmp/{fname}', 'collector-storage', f'kari/{stamp.year}/{stamp.month}/{stamp.day}/{stamp.hour}/{fname}',
                                ExtraArgs={'Metadata': {'footprint': footprint}})
    except ClientError as e:
        print(e)
        return False
    return True

def conv_obj(obj):
    url = f"https://ksatdb.kari.re.kr/catalog/{obj['BROWLOCATION']}"
    footprint = obj["GEO_STASTEXT"]
    date = arrow.get(obj["CENTERTIME"],"YYYYMMDDHHmmssS")
    on_s3 = grab_image(url,footprint,date)
    return {
        "date": date.format(),
        "img": url,
        "footprint": footprint,
        "on_s3": on_s3
    }

def get_imgs(bbox):
    out = []
    d = pull_data(bbox)
    for obj in d["data"]:
        out.append(conv_obj(obj))
    return out

if __name__ == "__main__":
    #print(pull_data({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176]}))
    print(get_imgs({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176]}))