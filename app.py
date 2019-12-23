import sqlite3
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
import pandas as pd


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
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)


with sqlite3.connect("db.db") as conn:
    cursor = conn.execute("""SELECT * FROM records""")
    columns = [x[0] for x in cursor.description]
    print(columns)
    init_table = cursor.fetchall()
    print(init_table)

    def clicked():
        res = f"{txt.get()}"
        lbl.configure(text=res)

    def free_query():
        res = f"{txt.get()}"

    window = Tk()
    window.title("wiseman")
    lbl = Label(window, text="Table", font=("Arial Bold", 24))
    lbl.pack()

    txt = Entry(window, width=10)
    txt.pack()

    combo_col = ttk.Combobox(window)
    combo_col["values"] = ("=", "<", ">", ">=", "<=")
    combo_col.current(0)
    combo_col.pack()

    combo = ttk.Combobox(window)
    combo["values"] = ("=", "<", ">", ">=", "<=")
    combo.current(0)
    combo.pack()

    btn = Button(window, text="Filter", command=clicked)
    btn.pack()

    table = Table(window, headings=columns, rows=init_table,)
    table.pack(expand=tk.YES, fill=tk.BOTH)

    window.mainloop()
