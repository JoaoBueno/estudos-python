# TESTE

import csv
import json

csvfile = open('1linha.csv', 'r')
jsonfile = open('1linha.json', 'w')

fieldnames = ('nivel', 'funcao', 'int', 'sep', 'opcao', 'prog')
reader = csv.DictReader(csvfile, fieldnames, delimiter=';')
for row in reader:
    print(row['opcao'])
    json.dump(row, jsonfile)
    jsonfile.write('\n')
