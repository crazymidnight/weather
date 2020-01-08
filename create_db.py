import sqlite3

import pandas as pd

data = pd.read_json("test.json")

print(data.columns)

to_use = [
    "listing_id",
    "created",
    "bathrooms",
    "bedrooms",
    "latitude",
    "longitude",
    "price",
    "photos",
    "description",
    "display_address",
    "street_address",
]

data = data.loc[:100, to_use]

data["photos"] = data["photos"].apply(len)
print(data["photos"])
data["description"] = data["description"].apply(len)
print(data["description"])

with sqlite3.connect("db.db") as conn:
    data.loc[:, ["listing_id", "bathrooms", "bedrooms"]].to_sql(
        name="rooms", con=conn, if_exists="replace"
    )
    data.loc[:, ["listing_id", "created", "photos", "description"]].to_sql(
        name="meta", con=conn, if_exists="replace"
    )
    data.loc[:, ["listing_id", "latitude", "longitude"]].to_sql(
        name="geo", con=conn, if_exists="replace"
    )
    data.loc[:, ["listing_id", "display_address", "street_address"]].to_sql(
        name="address", con=conn, if_exists="replace"
    )
    data.loc[:, ["listing_id", "price"]].to_sql(
        name="price", con=conn, if_exists="replace"
    )
    print(conn.execute("SELECT * FROM rooms").fetchall())
