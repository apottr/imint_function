from satimg.kari import get_imgs as kari
from satimg.landsat import get_imgs as landsat
from satimg.scihub import get_imgs as scihub
import json

def get_satimg(bbox):
    try:
        k = kari(bbox)
    except:
        k = []
    try:
        s = scihub(bbox)
    except:
        s = []
    try:
        l = landsat(bbox)
    except:
        l = []
    return {
        "kari": k,
        "scihub": s,
        "landsat": l
    }