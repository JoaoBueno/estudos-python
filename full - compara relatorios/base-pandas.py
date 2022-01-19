import sys
import os
import csv
import pandas as pd

def processa(arq):
    comfile = open(arq + '.ori', 'r')
    csvfile = open(arq + '.csv', 'w')


    def tiraespaco(l):
        l = l.replace(' ', '')
        l = l.replace('.', '')
        return l


    cab = ''
    ven = False
    for l in comfile:
        if len(cab) < 1:
            if l[:52] == '| NUMERO  |                 CLIENTE                |':
                l = tiraespaco(l)
                cab = l
                csvfile.write(l[1:-2] + '\n')
                # csvfile.write(l)

        if l[0:30] == '|TOTAL DO TIPO =====> MONTADOR':
            ven = True

        if ven:
            if l[52:70] == 'TOTAL DA NOTA ==> ':
                csvfile.write(l[1:-3] + '\n')

    comfile.close()
    csvfile.close()

    df = pd.read_csv(arq + '.csv', sep='|', encoding='cp1252', decimal=',')

    print(df.dtypes)
    print(df)

    df['VRBRUTO'] = [x.replace('.', '') for x in df['VRBRUTO']]
    df['VRBRUTO'] = [x.replace(',', '.') for x in df['VRBRUTO']]
    df['VRBRUTO'] = [x.replace(' ', '0') for x in df['VRBRUTO']]
    df['VRBRUTO'] = df['VRBRUTO'].astype(float)

    df['DESCONTO'] = [x.replace('.', '') for x in df['DESCONTO']]
    df['DESCONTO'] = [x.replace(',', '.') for x in df['DESCONTO']]
    df['DESCONTO'] = [x.replace(' ', '0') for x in df['DESCONTO']]
    df['DESCONTO'] = df['DESCONTO'].astype(float)

    df['VALORTROCA'] = [x.replace('.', '') for x in df['VALORTROCA']]
    df['VALORTROCA'] = [x.replace(',', '.') for x in df['VALORTROCA']]
    df['VALORTROCA'] = [x.replace(' ', '0') for x in df['VALORTROCA']]
    df['VALORTROCA'] = df['VALORTROCA'].astype(float)

    df['DEVOLUCAO'] = [x.replace('.', '') for x in df['DEVOLUCAO']]
    df['DEVOLUCAO'] = [x.replace(',', '.') for x in df['DEVOLUCAO']]
    df['DEVOLUCAO'] = [x.replace(' ', '0') for x in df['DEVOLUCAO']]
    df['DEVOLUCAO'] = df['DEVOLUCAO'].astype(float)

    df['VALORLIQUIDO'] = [x.replace('.', '') for x in df['VALORLIQUIDO']]
    df['VALORLIQUIDO'] = [x.replace(',', '.') for x in df['VALORLIQUIDO']]
    df['VALORLIQUIDO'] = [x.replace(' ', '0') for x in df['VALORLIQUIDO']]
    df['VALORLIQUIDO'] = df['VALORLIQUIDO'].astype(float)

    print(df.dtypes)
    print(df)

    print(sum(df.VRBRUTO))
    print(sum(df.DESCONTO))
    print(sum(df.VALORTROCA))
    print(sum(df.DEVOLUCAO))
    print(sum(df.VALORLIQUIDO))

    for index, row in df.iterrows():
        print(row['NUMERO'], row['VALORLIQUIDO'])

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Use: le-comissao arquivo")
        sys.exit(0)
    if os.path.isfile(sys.argv[1]):
        print(os.path.splitext(os.path.basename(sys.argv[1]))[0])
        # processa(sys.arqv[1])
    else:
        print(u'Arquivo não encontrado!')
        sys.exit(0)
    sys.exit(1)                                             