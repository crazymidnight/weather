import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from os import path
from tkinter import *
from tkinter import filedialog

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import pandas as pd
import xarray as xr
from metpy.testing import get_test_data
from metpy.units import units


class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = headings

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert("", tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        scrollcolumns = tk.Scrollbar(self, command=table.xview, orient=tk.HORIZONTAL)
        table.configure(
            xscrollcommand=scrollcolumns.set, yscrollcommand=scrolltable.set
        )
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        scrollcolumns.pack(side=tk.BOTTOM, fill=tk.X)
        table.pack(expand=tk.YES, fill=tk.BOTH)


def import_file():
    lbl.configure(text="Uploading to database")
    print(__file__)
    file = filedialog.askopenfilename(initialdir=path.dirname(__file__))
    data = xr.open_dataset(file)
    data = data.metpy.parse_cf()

    data = data.metpy.parse_cf()

    data["t2m"].metpy.convert_units("degC")
    data = data.to_dataframe().reset_index()
    data = data.drop(columns="crs")
    data["year"] = data["time"].apply(lambda x: x.year)
    data["month"] = data["time"].apply(lambda x: x.month)

    lat = data["latitude"].unique()
    lon = data["longitude"].unique()
    lat = {lat[v]: v for v in range(len(lat))}
    lon = {lon[v]: v for v in range(len(lon))}
    year = data["year"].unique()
    month = data["month"].unique()
    year = {year[v]: v for v in range(len(year))}
    month = {month[v]: v for v in range(len(month))}

    data["lat_id"] = data["latitude"].apply(lambda x: lat[x])
    data["lon_id"] = data["longitude"].apply(lambda x: lon[x])
    data["year_id"] = data["year"].apply(lambda x: year[x])
    data["month_id"] = data["month"].apply(lambda x: month[x])

    latitude = pd.DataFrame(data["latitude"].unique(), columns=["latitude"])
    longitude = pd.DataFrame(data["longitude"].unique(), columns=["longitude"])
    year = pd.DataFrame(data["year"].unique(), columns=["year"])
    month = pd.DataFrame(data["month"].unique(), columns=["month"])
    temperature = data.drop(columns=["time", "latitude", "longitude", "year", "month"])
    temperature = temperature.rename(columns={"t2m": "temperature"})

    with sqlite3.connect("weather.db") as conn:
        latitude.to_sql("latitude", con=conn, if_exists="replace")
        longitude.to_sql("longitude", con=conn, if_exists="replace")
        year.to_sql("year", con=conn, if_exists="replace")
        month.to_sql("month", con=conn, if_exists="replace")
        temperature.to_sql("temperature", con=conn, if_exists="replace")

    show_table()


def show_table():
    lbl.configure(text="Temperature by coordinates and time")
    cursor = conn.execute(
        """SELECT temperature.temperature, latitude.latitude, longitude.longitude, year.year, month.month
        FROM temperature
        JOIN latitude ON (temperature.lat_id = latitude.'index')
        JOIN longitude ON (temperature.lon_id = longitude.'index')
        JOIN year ON (temperature.year_id = year.'index')
        JOIN month ON (temperature.month_id = month.'index') LIMIT 100"""
    )
    columns = [x[0] for x in cursor.description]
    init_table = cursor.fetchall()
    if isinstance(table[0], Table):
        table[0].forget()
    table[0] = Table(tab_1, headings=columns, rows=init_table)
    table[0].pack(expand=tk.YES, fill=tk.BOTH)


with sqlite3.connect("weather.db") as conn:

    window = Tk()
    window.title("wiseman weather")

    tab_control = ttk.Notebook(window)
    tab_1 = ttk.Frame(tab_control)

    tab_control.add(tab_1, text="Data import")

    lbl = Label(tab_1, text="Upload file via button", font=("Arial Bold", 24))
    lbl.pack()

    btn_import = Button(tab_1, text="Import file", command=import_file)
    btn_import.pack()

    btn_show = Button(tab_1, text="Show table", command=show_table)
    btn_show.pack()

    table = [0]

    tab_control.pack(expand=1, fill="both")
    window.mainloop()
