import os
import csv
import sqlite3

arqC = 'b-co.csv'
arqF = 'b-fi-v.csv'

# arqC = (os.path.splitext(os.path.basename(arqC))[0])
# arqF = (os.path.splitext(os.path.basename(arqF))[0])

con = sqlite3.connect('compara.db3')
cur = con.cursor()

cur.execute('DROP TABLE arqC;')
cur.execute('CREATE TABLE arqC (numero integer PRIMARY KEY AUTOINCREMENT NOT NULL, valor float);')

with open(arqC, 'r') as fin:
    dr = csv.DictReader(fin, delimiter='|') 
    to_db = [(i['NUMERO'], i['VALORLIQUIDO']) for i in dr]

cur.executemany("INSERT INTO arqC (numero, valor) VALUES (?, ?);", to_db)
con.commit()


cur.execute('DROP TABLE arqF;')
cur.execute('CREATE TABLE arqF (numero integer NOT NULL, item integer NOT NULL, valor float, PRIMARY KEY(numero, item));')

with open(arqF, 'r') as fin:
    dr = csv.DictReader(fin, delimiter='|') 
    to_db = [(i['NUMERO'], i['PARCELA'], i['VALOR']) for i in dr]

cur.executemany("INSERT INTO arqF (numero, item, valor) VALUES (?, ?, ?);", to_db)
con. commit()

con.close()

