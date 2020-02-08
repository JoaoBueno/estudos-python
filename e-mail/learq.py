def learq(arqlog):
    hora = []
    sent = []
    tota = []

    arq = open(arqlog, 'r', encoding='utf-8')

    for linha in arq:
        valores = linha.split()
        if len(valores) > 0:
            if valores[0] == 'sent':
                sent.append(linha[:-1])
            if valores[0] == 'total':
                tota.append(linha[:-1])
        if len(valores) > 4:
            if valores[4] == 'BRST':
                hora.append(linha[:-1])
                # print(valores)

    arq.close()

    return(hora, sent, tota)