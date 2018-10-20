from flask import Flask,render_template,jsonify
import sqlite3
app = Flask(__name__)

@app.route("/")
def page():
    return render_template("index.html")

@app.route("/data")
def data():
    out = {"data": []}
    conn = sqlite3.connect("cameras.db")
    c = conn.cursor()
    c.execute("select lat,lon from cameras")
    for row in c.fetchall():
        out["data"].append({"lat": row[0], "lon": row[1]})
    return jsonify(out)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")