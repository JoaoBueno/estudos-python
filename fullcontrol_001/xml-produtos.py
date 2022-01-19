#!/usr/bin/python3

import os
import sys
import xmltodict
from collections import OrderedDict

with open('xmls/importar_produtos.xml', 'rb') as arquivo:
# with open('nfe.xml', 'rb') as arquivo:
    dados = arquivo.read().decode('UTF-8')
    doc = xmltodict.parse(dados)
    # print(doc)
    skus = []
    for sku in doc['root']['produto']:
        skus.append(sku['sku'])

print(skus)
print(sorted(set(skus)))
print(len(skus))

