import sys
import os
import csv
import pandas as pd


def procComissao(arq):
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
            if l[:62] == '| NUMERO  | NUMERON |                 CLIENTE                |':
                l = tiraespaco(l)
                cab = l
                csvfile.write(l[1:8] + 'TIPO|' + l[8:24] + l[29:-2] + '\n')

        if l[0:30] == '|TOTAL DO TIPO =====> MONTADOR':
            ven = True

        if ven:
            if l[62:80] == 'TOTAL DA NOTA ==> ':
                csvfile.write(l[1:9] + '|' + l[9:10] +
                              l[10:62] + l[81:-3] + '\n')

    comfile.close()
    csvfile.close()

    df = pd.read_csv(arq + '.csv', sep='|', encoding='cp1252', decimal=',')

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

    return df


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Use: leComissao arquivo")
        sys.exit(0)
    if os.path.isfile(sys.argv[1]):
        df = procComissao(os.path.splitext(os.path.basename(sys.argv[1]))[0])
        print(df)
    else:
        print(u'Arquivo nao encontrado!')
        sys.exit(0)
    sys.exit(1)
