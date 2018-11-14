from flask import Flask,render_template,jsonify,request,Response
from satimg import get_satimg as satimg
from camimg import get_cameras as camimg
from os import environ as env
import json,requests
app = Flask(__name__)

@app.route("/")
def page():
    return render_template("index.html")

def runner(bbox):
    s = satimg(bbox)
    c = camimg(bbox)
    return {"data": s+c}

@app.route("/data", methods=["POST"])
def data():
    bbox = json.loads(request.form["box"])
    o = runner(bbox)
    return jsonify(o)

@app.route("/img/<path:url>")
def image_grabber(url):
    if "scihub" in url:
        r = requests.get(url,auth=(env["SH_USER"],env["SH_PASS"]))
    else:
        r = requests.get(url)
    return Response(r.content,mimetype=r.headers['content-type'].split(";")[0])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")