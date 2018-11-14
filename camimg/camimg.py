import pandas as pd
import geopandas as gp
from geopandas.geoseries import GeoSeries
from shapely.geometry import Point,Polygon
import sqlite3
from pathlib import Path

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


if __name__ == "__main__":
    #print(get_cameras({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))
    pass
