import sqlite3
import pandas as pd

data = pd.read_json("test.json")

print(data.columns)

to_use = [
    "listing_id",
    "bathrooms",
    "bedrooms",
    "latitude",
    "longitude",
    "price",
]
data = data.loc[:30, to_use]


with sqlite3.connect("db.db") as conn:

    data.to_sql(name="records", con=conn, if_exists="replace")
    print(conn.execute("SELECT * FROM records").fetchall())
    print(conn.execute("SELECT * FROM records").fetchall())
