#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Este documento é uma rápida introdução ao SQLAlchemy.
#
#   SQLAlchemy is the Python SQL toolkit and Object Relational Mapper 
#   that gives application developers the full power and flexibility of SQL.
#
#   It provides a full suite of well known enterprise-level persistence patterns, 
#   designed for efficient and high-performing database access, adapted into a 
#   simple and Pythonic domain language.
#
# Ao escrever isso estou usando python 2.6 e sqlalchemy 0.5.5.
# Como exemplo vou organizar a coleção de discos. 

m = input("Mostrar sql gerado?[s/n] ")
mostrar = [True, False][m.lower() == 'n']
espera = mostrar
    

############# PASSO 1 - CRIAR UMA CONEXÃO COM O BANCO DE DADOS. ################

# O banco de dados usado será o sqlite.
# O sqlalchemy usa um objeto 'engine' para se conectar ao banco de dados.
from sqlalchemy import create_engine

#O parametro 'echo = True' faz com que o sql gerado seja mostrado na tela.
engine = create_engine('sqlite:///discoteca.db', echo = mostrar) 


########### PASSO 2 - CRIAR AS TABELAS QUE SERÃO USADAS. #######################

#Uma tabela no sqlalchemy é um objeto do tipo Table. 
#objetos do tipo Column são usados para definir os campos da tabela.
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData

# MetaData é o objeto responsável pelas queries e orm.
metadata = MetaData()

tabela_bandas = Table('bandas', metadata,
    Column('id', Integer, primary_key = True),
    Column('nome', String),
    Column('lugar', String)
)

#Um disco pode ter mais de uma banda.
tabela_discos = Table('discos', metadata,
    Column('id', Integer, primary_key = True),
    Column('nome', String),
    Column('ano', Integer)
)

tabela_discos_bandas = Table('discos_bandas', metadata,
    Column('id', Integer, primary_key = True),
    Column('id_banda', Integer, ForeignKey('bandas.id')),
    Column('id_disco', Integer, ForeignKey('discos.id')),
)

#Neste exemplo uma música só está em um único disco.
tabela_musicas = Table('musicas', metadata,
    Column('id', Integer, primary_key = True),
    Column('id_disco', Integer, ForeignKey('discos.id')),
    Column('id_banda', Integer, ForeignKey('bandas.id')),
    Column('numero', Integer),
    Column('nome', String)
)

#Como as tabelas não existem, as criaremos usando a nossa instância de MetaData().
#Nossa engine (criada no passo 1) será passada como parametro.
metadata.create_all(engine)
if espera:
    input("\nO SQL gerado foi a criação das  tabelas.")

# Conexão com o banco de dados estabelecida, tabelas criadas... 
#Agora é hora de definir nossos objetos.




####### PASSO 3 - CRIAR AS CLASSES E MAPEÁ-LAS COM AS TABELAS CRIADAS. #########

#Para mapear as classes com as tabelas usaremos o método mapper() 
#A sintaxe do mapper é a seginte: mapper(classe, tabela).
#Com isso, associa-se a classe à tabela.

from sqlalchemy.orm import mapper, relation

class musica(object):
    def __repr__(self):
        numero = self.numero or 0
        nome = self.nome or ''
        if self.disco:
            disco = self.disco.nome
        else:
            disco = ''
        return """numero: %i, nome: %s, disco: %s""" %(numero, nome, disco)

#mapeando musica com tabela_musicas.
mapper(musica, tabela_musicas)


class banda(object):
    def __repr__(self):
        nome = self.nome or ''
        lugar = self.lugar or ''
        return """nome: %s, lugar: %s""" %(nome, lugar)
        
#mapeando banda com tabela_bandas.
#Definiremos também a relação banda/musica usando relation(),
#'backref' cria a relação também 'do lado contrário'. 
#O parâmetro 'properties' cria atributos para a classe que está sendo mapeada.
mapper(banda, tabela_bandas,
       properties = {'musicas' : relation(musica, backref = 'banda')}
       )



class disco(object):
    def __repr__(self):
        nome = self.nome or ''
        ano = self.ano or 0
        if self.bandas:
            banda = ','.join([i.nome for i in self.bandas])
        else:
            banda = ''
        return """nome: %s, ano: %s, banda: %s""" %(nome, str(ano), banda)
        
#Mapeando disco com tabela_discos, onde definiremos também relacionamentos.
#A relação bandas/discos é muitos-para-muitos. Por isso foi passado o parâmetro
#'secondary'.
mapper(disco, tabela_discos, 
       properties = {'musicas' : relation(musica, backref = 'disco'), 
                     'bandas'  : relation(banda, 
                                          secondary = tabela_discos_bandas, 
                                          backref = 'discos')
                     }
       )


#Já está tudo criado, os objetos mapeados... Vamos brincar com a coisa!


###################### BRINCANDO COM OS NOSSOS OBJETOS  ########################


#Primeiro instanciar banda() e cadastrar uma nova banda.
#Repare que os atributos do objeto são as colunas da tabela (da hora, né!) .
nova_banda = banda()
nova_banda.nome = "Tankard"
nova_banda.lugar = "Frankfurt"

#Bom, uma nova banda foi criada aí, mas ainda não foi salva no banco. 
#Para salvar no banco usaremos um objeto 'session' que será criado com sessionmaker
#Nossa 'session' será associada à nossa 'engine'.
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

#Agora, com a session criada, é só adicionar nosso objeto a session...
session.add(nova_banda)
# ...e 'commitar' a coisa.
session.commit()
if espera:
    input("\nEste sql é da inserção de uma banda.")

#Pronto, objeto salvo. Agora vamos recuperá-lo. 
#Usaremos o método session.query() para fazer isso.
uma_banda = session.query(banda).filter(banda.nome == "Tankard").first()
if espera:
    input("\nEste aqui é a recuperação de uma banda.")

#Bom, vamos criar um disco.
novo_disco = disco()
novo_disco.nome = "The Morning After"
novo_disco.ano = 1988
session.add(novo_disco)
session.commit()

#Um disco tem músicas, não?
musicas = ['Intro', 'Commandment', 'Shit-faced', 'TV Hero', 'F.U.N.',
           'Try Again', 'The Morning After', 'Desperation',
           'Feed the Lohocla', 'Help Yourself', 'Mon Cheri', 'Outro']
i = 1
for m in musicas:
    nova_musica = musica()
    nova_musica.nome = m
    nova_musica.banda = uma_banda
    nova_musica.numero = i
    i += 1
    #Lembra do relation(), backref e tal que falei lá em cima? Então, olha aí!
    #O atributo nova_musica.disco aí embaixo foi criado com eles. 
    nova_musica.disco = novo_disco
    session.add(nova_musica)
    session.commit()

#Usando novamente um atributo criado na configuração do mapper...
uma_banda.discos.append(novo_disco)

#Bom, vamos cadastrar mais umas coisas aí pra entender direitinho como funciona.
rdp = banda()
rdp.nome = u"Ratos de Porão"
rdp.lugar = u"São Paulo"

cl = banda()
cl.nome = u"Cólera"
cl.lugar = u"São Paulo"

pk = banda()
pk.nome = u"Psykóze"
pk.lugar = u"São Paulo"

fc = banda()
fc.nome = u"Fogo Cruzado"
fc.lugar = u"São Paulo"

outro_disco = disco()
outro_disco.nome = "Sub"
outro_disco.bandas.append(rdp)
outro_disco.bandas.append(cl)
outro_disco.bandas.append(pk)
outro_disco.bandas.append(fc)
session.add(outro_disco)
#session.commit()

musicas_sub = [(u'Parasita', rdp), (u'Vida Ruim', rdp), (u"Poluição Atômica", rdp),
               (u"X.O.T.", cl), (u"Bloqueio Mental", cl),
               (u"Quanto Vale a Liberdade", cl), (u"Terceira Guerra Mundial", pk),
               (u"Buracos Suburbanos", pk), (u"Fim do Mundo", pk),
               (u"Desemprego", fc), (u"União entre os Punks do Brasil", fc),
               (u"Delinqüentes", fc), (u"Não Podemos Falar", rdp),
               (u"Realidades da Guerra", rdp), (u"Porquê?", rdp), (u"Histeria", cl),
               (u"Zero zero", cl), (u"Sub-ratos", cl), (u"Vítimas da Guerra", pk),
               (u"Alienação do Homem", pk), (u"Desilusão", pk), (u"Inimizade", fc),
               (u"Punk Inglês", fc), (u"Terceira Guerra", fc)]

i = 1
for m in musicas_sub:
    nova_musica = musica()
    nova_musica.nome = m[0]
    nova_musica.banda = m[1]
    nova_musica.numero = i
    session.add(nova_musica)
    session.commit()
    nova_musica.disco = outro_disco
    i += 1


#Agora que já criamos as paradas, vamos ver...
bandas = session.query(banda).all()
for b in bandas:
    print("Banda: " , b.nome)
    for d in b.discos:
        print("  Disco: ", d.nome)
        for m in d.musicas:
            if m.banda.id == b.id:
                print("    Música: ", m.nome)