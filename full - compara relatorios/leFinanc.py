import sys
import os
import csv
import pandas as pd


def procFinanc(arq):
    comfile = open(arq + '.ori', 'r')
    csvfile = open(arq + '.csv', 'w')

    cab = 'EMPRESA|ESPECIE|SERIE|NUMERO|PARCELA|VALOR'
    csvfile.write(cab + '\n')

    for l in comfile:
        if l[47:48] == '5' and l[49:50] == '/' and l[53:54] == '/':
            csvfile.write(l[47:49] + '|' + 
                          l[50:53] + '|' + 
                          l[54:57] + '|' + 
                          l[58:66] + '|' + 
                          l[67:69] + '|' + 
                          l[89:102] + '\n')

    comfile.close()
    csvfile.close()

    df = pd.read_csv(arq + '.csv', sep='|', encoding='cp1252', decimal=',')

    df['VALOR'] = [x.replace('.', '') for x in df['VALOR']]
    df['VALOR'] = [x.replace(',', '.') for x in df['VALOR']]
    df['VALOR'] = [x.replace(' ', '0') for x in df['VALOR']]
    df['VALOR'] = df['VALOR'].astype(float)

    return df


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Use: leFinanc arquivo")
        sys.exit(0)
    if os.path.isfile(sys.argv[1]):
        df = procFinanc(os.path.splitext(os.path.basename(sys.argv[1]))[0])
        print(df)
    else:
        print(u'Arquivo não encontrado!')
        sys.exit(0)
    sys.exit(1)
