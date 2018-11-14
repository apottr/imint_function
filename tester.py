from satimg import get_satimg as satimg
from camimg import get_cameras as camimg
def runner(bbox):
    s = satimg(bbox)
    c = camimg(bbox)
    return s+c

if __name__ == "__main__":
    print(runner({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] }))