from kari import get_imgs as kari
from scihub import get_imgs as scihub
from landsat import get_imgs as landsat
import json

def get_satimg(bbox):
    k = kari(bbox)
    s = scihub(bbox)
    l = landsat(bbox)
    return json.dumps({"data": k+s+l})

if __name__ == "__main__":
    bbox = {"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }
    #nw,se = bbox["nw"],bbox["se"]
    #print(f"POLYGON(({nw[0]} {nw[1]}, {se[0]} {nw[1]}, {se[0]} {se[1]}, {nw[0]} {se[1]}, {nw[0]} {nw[1]}))")
    print(get_satimg(bbox))




    