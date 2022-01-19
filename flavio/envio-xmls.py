#!/usr/bin/python3

import os
import lepasta 
import zipfile
from datetime import datetime
from six.moves import configparser
from envia_email import envia_email

def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)


anomes = datetime.today()
anomes = monthdelta(anomes, -1).strftime('%Y%m')

cfg = configparser.ConfigParser()
cfg.read('xmls.ini')

pasta = cfg.get('xmls', 'pasta').format(anomes=anomes)

lista = lepasta.monta_lista(pasta)

arqrar = anomes + '.rar'
 
compacta = zipfile.ZipFile(arqrar, 'w')

for nome in lista:
    compacta.write(nome, compress_type = zipfile.ZIP_DEFLATED)    
    
compacta.close()
    
    
envia_email('teste@bellasoft.com.br', ['teste@bellasoft.com.br','flavio@bellasoft.com.br','fiscal.diskepi@gmail.com'], 'XMLS - ' + anomes, 'Segue em anexo os arquivos xmls do mes ' + anomes, [arqrar])

os.remove(arqrar)
