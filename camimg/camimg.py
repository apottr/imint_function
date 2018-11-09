import pandas as pd
import geopandas as gp
from geopandas.geoseries import GeoSeries
from shapely.geometry import Point,Polygon

def load_cameras():
    df = pd.read_csv("out.csv")
    return df

def to_geopandas(df):
    gdf = df
    gdf["geometry"] = gdf.apply(lambda z: Point(z.lat, z.lon), axis=1)
    gdf = gp.GeoDataFrame(gdf)
    return gdf

def bbox_intersects(gdf,bbox):
    nw,se = bbox["nw"],bbox["se"]
    bounds = GeoSeries([Polygon([(nw[0],nw[1]),(se[0],nw[1]),(se[0],se[1]),(nw[0],se[1])])])
    filtered = gdf["geometry"].intersects(bounds.unary_union)
    return filtered.values[filtered == True]

def get_cameras(bbox):
    d = load_cameras()
    g = to_geopandas(d)
    o = bbox_intersects(g,bbox)
    return o

if __name__ == "__main__":
    print(get_cameras({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))
