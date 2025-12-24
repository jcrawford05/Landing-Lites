import sqlite3
import json

DB_PATH = "Airports.db"
OUT_PATH = "airports_nested.json"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

airports = [dict(r) for r in cur.execute("SELECT * FROM Airports")]
runways  = [dict(r) for r in cur.execute("SELECT * FROM Runways")]

def normalize(rows):
    return [
        {k.replace(" ", "_").replace(".", "_"): v for k, v in row.items()}
        for row in rows
    ]

airports = normalize(airports)
runways  = normalize(runways)

runways_by_airport = {}
for r in runways:
    runways_by_airport.setdefault(r.get("Airport_Ref_"), []).append(r)

for a in airports:
    a["Runways"] = runways_by_airport.get(a.get("ID"), [])

result = {"Airports": airports}

with open(OUT_PATH, "w") as f:
    json.dump(result, f, indent=2)

print(f"Wrote {OUT_PATH}")
