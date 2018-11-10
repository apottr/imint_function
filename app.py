from flask import Flask,render_template,jsonify,request
from satimg import get_satimg as satimg
import json
app = Flask(__name__)

@app.route("/")
def page():
    return render_template("index.html")

@app.route("/data", methods=["POST"])
def data():
    bbox = json.loads(request.form["box"])
    o = satimg(bbox)
    return jsonify(o)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")