import csv
import os
import pandas as pd

arq = 'b-fi-v'

comfile = open(arq + '.ori', 'r')
csvfile = open(arq + '.csv', 'w')


def tiraespaco(l):
    l = l.replace(' ', '')
    l = l.replace('.', '')
    return l


cab = 'NOTA|VALOR'
csvfile.write(cab + '\n')
ven = False
for l in comfile:
    if l[47:48] == '5' and l[49:50] == '/' and l[53:54] == '/':
        print(l[47:69] + '|' + l[89:102])
        csvfile.write(l[47:69] + '|' + l[89:102] + '\n')

comfile.close()
csvfile.close()

df = pd.read_csv(arq + '.csv', sep='|', encoding='cp1252', decimal=',')

print(df.dtypes)
print(df)

df['VALOR'] = [x.replace('.', '') for x in df['VALOR']]
df['VALOR'] = [x.replace(',', '.') for x in df['VALOR']]
df['VALOR'] = [x.replace(' ', '0') for x in df['VALOR']]
df['VALOR'] = df['VALOR'].astype(float)

print(df.dtypes)
print(df)

print(sum(df.VALOR))