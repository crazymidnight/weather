import sqlite3
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk


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

    def filtered():
        query = (
            f"SELECT * FROM records WHERE {combo_col.get()} {combo.get()} {txt.get()}"
        )
        cursor = conn.execute(query)
        headings = [x[0] for x in cursor.description]
        rows = cursor.fetchall()
        table[0].forget()
        table[0] = Table(window, headings=columns, rows=rows)
        table[0].pack(expand=tk.YES, fill=tk.BOTH)

    window = Tk()
    window.title("wiseman")
    lbl = Label(window, text="Table", font=("Arial Bold", 24))
    lbl.pack()

    combo_col = ttk.Combobox(window)
    combo_col["values"] = columns
    combo_col.current(1)
    combo_col.pack()

    combo = ttk.Combobox(window)
    combo["values"] = ("=", "!=", "<", ">", ">=", "<=")
    combo.current(0)
    combo.pack()

    txt = Entry(window, width=10)
    txt.pack()

    btn = Button(window, text="Filter", command=filtered)
    btn.pack()

    table = [Table(window, headings=columns, rows=init_table)]
    table[0].pack(expand=tk.YES, fill=tk.BOTH)

    window.mainloop()
