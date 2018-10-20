import sqlite3,csv

def reader():
    conn = sqlite3.connect("cameras.db")
    c = conn.cursor()
    c.execute("select lat,lon,id from cameras")
    for row in c:
        yield {"lat": row[0], "lon": row[1], "id": row[2]}

def writer():
    with open("out.csv", 'w') as csvfile:
        fieldnames = ["lat","lon","id"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader():
            writer.writerow(row)

if __name__ == "__main__":
    writer()