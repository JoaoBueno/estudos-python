#!/usr/bin/python3

import learq
from datetime import datetime
from envia_email import envia_email

arqlog = '/dados/sistema/backup/rsync.log'

hora, sent, tota = learq.learq(arqlog)

status = ''
stacor = '#00B050'
data_inicio = ''
hora_inicio = ''
enviado = ''
hora_fim = ''
data_size = ''
tempo_total = ''
velocidade = ''

if len(hora) == 2 or len(hora) == 4:
    status = 'Sucesso'
    if len(hora) > 2:
        data_inicio = hora[2]
        data_fim = hora[3]
        sent_ = sent[1]
        tota_ = tota[1]
    else:
        data_inicio = hora[0]
        data_fim = hora[1]
        sent_ = sent[0]
        tota_ = tota[0]

    hora_inicio = data_inicio.split()[3]
    hora_fim = data_fim.split()[3]
    enviado = sent_.split()[1] + ' ' + sent_.split()[2]
    data_size = tota_.split()[3] + ' ' + sent_.split()[2]
    hor_ini = datetime.strptime(hora_inicio, '%H:%M:%S')
    hor_fim = datetime.strptime(hora_fim, '%H:%M:%S')
    tempo_total = hor_fim - hor_ini
    velocidade = sent_.split()[6] + ' ' + sent_.split()[7]
else:
    status = 'Falhou'
    stacor = '#ff1030'
    data_inicio = 'Verifique arquivo em anexo'

template = open('template.html', 'r', encoding='utf-8').read().format(status=status,
                                                                      stacor=stacor,
                                                                      data_inicio=data_inicio,
                                                                      hora_inicio=hora_inicio,
                                                                      enviado=enviado,
                                                                      hora_fim=hora_fim,
                                                                      data_size=data_size,
                                                                      tempo_total=tempo_total,
                                                                      velocidade=velocidade)

envia_email('backup@1linha.com.br', ['notifyti@multip.com.br','bueno@1linha.com.br'], 'Backup 1linhasrv', template, [arqlog])
