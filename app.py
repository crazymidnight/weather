import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


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


with sqlite3.connect("db.db") as conn:
    conn.execute("""DROP TABLE records""")
    conn.execute(
        """
        CREATE TABLE records AS
        SELECT rooms.*, geo.latitude, geo.longitude, address.display_address,
        address.street_address, meta.created, meta.photos, meta.description, price.price
        FROM rooms 
        JOIN geo ON (rooms.listing_id = geo.listing_id)
        JOIN address ON (rooms.listing_id = address.listing_id)
        JOIN meta ON (rooms.listing_id = meta.listing_id)
        JOIN price ON (rooms.listing_id = price.listing_id)
        """
    )
    cursor = conn.execute("""SELECT * FROM records""")
    columns = [x[0] for x in cursor.description]
    init_table = cursor.fetchall()
    df = pd.DataFrame(init_table, columns=columns)

    def filtered():
        query = (
            f"SELECT * FROM records WHERE {combo_col.get()} {combo.get()} {txt.get()}"
        )
        cursor = conn.execute(query)
        headings = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        table[0].forget()
        table[0] = Table(tab_1, headings=columns, rows=rows)
        table[0].pack(expand=tk.YES, fill=tk.BOTH)

    def build_linear():
        plot_window = Tk()
        plot_window.title("linear plot")
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        sns.lineplot(df[x_col.get()], df[y_col.get()], ax=a)
        canvas = FigureCanvasTkAgg(f, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def build_trend():
        plot_window = Tk()
        plot_window.title("trend")
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        sns.regplot(df[x_col.get()], df[y_col.get()], x_estimator=np.mean, ax=a)
        canvas = FigureCanvasTkAgg(f, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def build_hist():
        plot_window = Tk()
        plot_window.title("histogram")
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        agg = df.groupby("bedrooms").apply(np.mean)
        sns.barplot(df[x_col.get()], df[y_col.get()], ax=a)
        canvas = FigureCanvasTkAgg(f, plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    window = Tk()
    window.title("wiseman")

    tab_control = ttk.Notebook(window)
    tab_1 = ttk.Frame(tab_control)
    tab_2 = ttk.Frame(tab_control)

    tab_control.add(tab_1, text="Data extracrion")
    tab_control.add(tab_2, text="Visualization")

    lbl = Label(tab_1, text="Table", font=("Arial Bold", 24))
    lbl.pack()

    combo_col = ttk.Combobox(tab_1)
    combo_col["values"] = columns
    combo_col.current(1)
    combo_col.pack()

    combo = ttk.Combobox(tab_1)
    combo["values"] = ("=", "!=", "<", ">", ">=", "<=")
    combo.current(0)
    combo.pack()

    txt = Entry(tab_1, width=10)
    txt.pack()

    btn = Button(tab_1, text="Filter", command=filtered)
    btn.pack()

    x_col = ttk.Combobox(tab_2)
    x_col["values"] = columns
    x_col.current(1)
    x_col.pack()

    y_col = ttk.Combobox(tab_2)
    y_col["values"] = columns
    y_col.current(2)
    y_col.pack()

    btn_plt = Button(tab_2, text="Plot", command=build_linear)
    btn_plt.pack()

    btn_hist = Button(tab_2, text="Hist", command=build_hist)
    btn_hist.pack()

    btn_trend = Button(tab_2, text="Trend", command=build_trend)
    btn_trend.pack()

    table = [Table(tab_1, headings=columns, rows=init_table)]
    table[0].pack(expand=tk.YES, fill=tk.BOTH)

    tab_control.pack(expand=1, fill="both")
    window.mainloop()
