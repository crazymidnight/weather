import sqlite3


with sqlite3.connect('db.db') as conn:
    conn.execute('''CREATE TABLE records (id INT, value INT)''')

    conn.execute('''INSERT INTO records VALUES (1, 25)''')

