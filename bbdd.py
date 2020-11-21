import sqlite3

conn = sqlite3.connect('sqlitedb.db')
c = conn.cursor()

c.execute('''CREATE TABLE stocks(date text, trans text, symbol text, qty real, price real)''')
c.execute('''INSERT INTO stocks VALUES('2006-01-05', 'BUY', 'RATH', 100, 35.14)''')

conn.commit()

c.execute('''SELECT * FROM stocks''')

for tupla in c.fetchall():
    print(tupla)

c.close()
conn.close()
