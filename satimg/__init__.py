from satimg.kari import get_imgs as kari
from satimg.landsat import get_imgs as landsat
from satimg.scihub import get_imgs as scihub
import json

def get_satimg(bbox):
    k = kari(bbox)
    s = scihub(bbox)
    l = landsat(bbox)
    return k+s+l