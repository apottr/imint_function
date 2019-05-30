import pandas as pd
import geopandas as gp
from geopandas.geoseries import GeoSeries
from shapely.geometry import Point,Polygon
import sqlite3,boto3,ast,arrow
from pathlib import Path
import botocore.vendored.requests as requests
from botocore.exceptions import ClientError

def load_cameras():
    cnx = sqlite3.connect(str(Path(__file__).parent / "cameras.db"))
    df = pd.read_sql_query("SELECT * FROM cameras",cnx)
    return df

def to_geopandas(df):
    gdf = df
    gdf["geometry"] = gdf.apply(lambda z: Point(float(z.lon), float(z.lat)), axis=1)
    gdf = gp.GeoDataFrame(gdf)
    return gdf

def bbox_intersects(gdf,bbox):
    nw,se = bbox["nw"],bbox["se"]
    return gdf.cx[nw[0]:se[0],nw[1]:se[1]]

def grab_img(url,footprint,stamp):
    fname = url.split('/')[-1]
    s3 = boto3.client('s3')
    with open(f"/tmp/{fname}","wb") as f:
        r = requests.get(url)
        f.write(r.content)
    try:
        resp = s3.upload_file(f'/tmp/{fname}', 'collector-storage', 
        f'traffic/{stamp.year}/{stamp.month}/{stamp.day}/{stamp.hour}/{fname}-{stamp.timestamp}',
                                ExtraArgs={'Metadata': {'footprint': footprint}})
    except ClientError as e:
        print(e)
        return False
    return True

def get_cameras(bbox):
    d = load_cameras()
    g = to_geopandas(d)
    o = bbox_intersects(g,bbox)
    out = []
    for i,entry in o.iterrows():
        url = ast.literal_eval(entry["format"])[0]
        footprint = entry["geometry"].wkt
        now = arrow.now()
        on_s3 = grab_img(url,footprint,now)
        out.append({
            "date": now.format(),
            "footprint": footprint,
            "img": url,
            "on_s3": on_s3
        })
    return out

if __name__ == "__main__":
    print(get_cameras({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))
    #pass
