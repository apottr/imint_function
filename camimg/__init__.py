from camimg.camimg import load_cameras,to_geopandas,bbox_intersects
import ast,arrow

def get_cameras(bbox):
    d = load_cameras()
    g = to_geopandas(d)
    o = bbox_intersects(g,bbox)
    out = []
    for i,entry in o.iterrows():
        out.append({
            "date": arrow.now().format(),
            "footprint": entry["geometry"].wkt,
            "img": ast.literal_eval(entry["format"])[0]
        })
    return out