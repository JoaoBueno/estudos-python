import os
import csv
import sqlite3
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import Integer, Float, CHAR
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select

csvC = 'b-co.csv'
csvF = 'b-fi-v.csv'

_url = 'sqlite:///compara.db3'
# para conexao no firebird
# _url = URL('firebird', 'SYSDBA', 'masterkey', '192.168.1.11', '3052', 'bdband')
# para conexao no mysql
# _url = 'mysql://usuario:senha@servidor/banco'

# cria o engine e metadata
engine = create_engine(_url, echo=False)
metadata = MetaData(bind=engine)

# cria as tabelas
tb_arqC = Table('arqC', metadata,
                Column('numero', Integer(), primary_key=True, nullable=False),
                Column('valor', Float()),
                Column('achou', CHAR())
                )

tb_arqF = Table('arqF', metadata,
                Column('numero', Integer(), primary_key=True, nullable=False),
                Column('item', Integer(), primary_key=True, nullable=False),
                Column('valor', Float()),
                Column('achou', CHAR())
                )

# cria as classes


class arqC(object):
    def __init__(self, numero, valor, achou=' '):
        self.numero = numero
        self.valor = valor
        self.achou = achou


class arqF(object):
    def __init__(self, numero, item, valor, achou=' '):
        self.numero = numero
        self.item = item
        self.valor = valor
        self.achou = achou


# mapeia a classe -> tabela
mapper(arqC, tb_arqC)
mapper(arqF, tb_arqF)

# cria as tabelas no banco (caso nao existam)
metadata.create_all()

conn = engine.connect()

# s = select([arqC])
# # result = conn.execute(s)

# for row in conn.execute(s):
#     print(row['numero'],row['valor'])
#     p = select([tb_arqF.c.numero, tb_arqF.c.valor]).where(tb_arqF.c.numero == row[tb_arqC.c.numero])
#     result = conn.execute(p)
#     for prow in result:
#         print(prow, result.count())
#         if row[tb_arqC.c.valor] == prow[tb_arqF.c.valor]:
#             print('ok')
#     input()

#cria o sessionmaker
Session = sessionmaker(bind=engine)

s = Session()

ttc = 0
ttf = 0

for c in s.query(arqC):
    print(c.numero)
    q = s.query(arqF).filter(arqF.numero == c.numero)
    qtd = 0
    tot = 0
    ttc = ttc + c.valor
    for f in q:
        qtd = qtd + 1
        tot = tot + f.valor
        print(c.numero, c.valor, f.numero, f.valor, q.count())
        if q.count() == qtd:
            if c.valor != tot:
                print('não ok')
                # input()
            else:
                c.achou = 'S'
                ttf = ttf + tot
                # s.commit()
                # input()

s.commit()      
print(ttc, ttf)          

# for row in s.query(arqC, arqF).filter(tb_arqC.c.numero == tb_arqF.c.numero):
#     print(row.arqC.numero, row.arqC.valor, row.arqF.valor)