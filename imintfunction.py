from satimg import get_satimg as satimg
from camimg import get_cameras as camimg
import json
def runner(bbox):
    s = satimg(bbox)
    c = camimg(bbox)
    s["cameras"] = c
    return s

def handler(event, context):
    b = json.loads(event["body"])
    return {"data": runner(b["bbox"])}

if __name__ == "__main__":
    print(json.dumps(runner({"nw": [-71.30126953125,42.53486817758702], "se": [-70.7958984375,42.204107493733176] })))