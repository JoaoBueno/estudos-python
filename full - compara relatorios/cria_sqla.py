import os
import csv
import sqlite3
from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import Integer, Float, CHAR
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy.engine.url import URL

csvC = 'b-co.csv'
csvF = 'b-fi-v.csv'

_url = 'sqlite:///compara.db3'
### para conexao no firebird
# _url = URL('firebird', 'SYSDBA', 'masterkey', '192.168.1.11', '3052', 'bdband')
### para conexao no mysql
# _url = 'mysql://usuario:senha@servidor/banco'

# cria o engine e metadata
engine = create_engine(_url, echo=True)
metadata = MetaData(bind=engine)

#cria as tabelas
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

#cria as classes
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

#cria as tabelas no banco (caso nao existam)
metadata.create_all()

#cria o sessionmaker
Session = sessionmaker(bind=engine)

s = Session()

insert_query = tb_arqC.insert()
with open(csvC, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='|')
    next(csv_reader)
    engine.execute(
        insert_query,
        [{'numero': int(row[2].strip()), 
          'valor': row[8].strip().replace('.', '').replace(',','.') if row[8].strip().replace('.', '').replace(',','.') else '0.0', 
          'achou': ' '} for row in csv_reader]
    )

insert_query = tb_arqF.insert()
with open(csvF, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter='|')
    next(csv_reader)
    engine.execute(
        insert_query,
        [{'numero': int(row[3].strip()), 
          'item': int(row[4].strip()), 
          'valor': row[5].strip().replace('.', '').replace(',','.') if row[5].strip().replace('.', '').replace(',','.') else '0.0', 
          'achou': ' '} for row in csv_reader]
    )

