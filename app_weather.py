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

    data["t2m"].metpy.convert_units("degC")
    lon, lat, time, temp = data["longitude"], data["latitude"], data["time"], data["t2m"]
    temp.to_series().to_sql(name="temp", con=conn, if_exists="replace")

    lbl.configure(text="Uploading is complete")
    cursor = conn.execute("""SELECT * FROM temp LIMIT 100""")
    columns = [x[0] for x in cursor.description]
    init_table = cursor.fetchall()
    table[0] = Table(tab_1, headings=columns, rows=init_table)
    table[0].pack(expand=tk.YES, fill=tk.BOTH)


with sqlite3.connect("weather.db") as conn:

    window = Tk()
    window.title("wiseman weather")

    tab_control = ttk.Notebook(window)
    tab_1 = ttk.Frame(tab_control)
    tab_2 = ttk.Frame(tab_control)

    tab_control.add(tab_1, text="Data import")
    tab_control.add(tab_2, text="Visualization")

    lbl = Label(tab_1, text="Upload file via button", font=("Arial Bold", 24))
    lbl.pack()

    btn_import = Button(tab_1, text="Import file", command=import_file)
    btn_import.pack()

    table = [0]

    tab_control.pack(expand=1, fill="both")
    window.mainloop()
