import os
import csv
import sqlite3
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import Integer, Float, CHAR
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.engine.url import URL
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base

csvC = 'b-co.csv'
csvF = 'b-fi-v.csv'

_url = 'sqlite:///compara.db3'
# para conexao no firebird
# _url = URL('firebird', 'SYSDBA', 'masterkey', '192.168.1.11', '3052', 'bdband')
# para conexao no mysql
# _url = 'mysql://usuario:senha@servidor/banco'

# cria o engine e metadata
engine = create_engine(_url, echo=False)
Base = declarative_base(bind=engine)


# cria as classes e tabelas ja mapeando
class arqC(Base):
    __tablename__ = 'arqC'

    numero = Column(Integer, primary_key=True)
    valor = Column(Float())
    achou = Column(CHAR())

    def __init__(self, numero, valor, achou=' '):
        self.numero = numero
        self.valor = valor
        self.achou = achou


class arqF(Base):
    __tablename__ = 'arqF'

    numero = Column(Integer, primary_key=True)
    item = Column(Integer, primary_key=True)
    valor = Column(Float())
    achou = Column(CHAR())

    def __init__(self, numero, item, valor, achou=' '):
        self.numero = numero
        self.item = item
        self.valor = valor
        self.achou = achou


Base.metadata.create_all()

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

# cria o sessionmaker
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
