#!/usr/bin/python3

import sys
import subprocess
import argparse
import re
import os
from operator import itemgetter

def isTime(time):
    """Verifica se e uma Hora valida"""
    if not re.match(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time):
        return(False)
    return(True)

def get_arguments():
    parser = argparse.ArgumentParser(description = 'Mata processos antigos')
    parser.add_argument('-k', '--kill', dest='simnao', help='Mata os processosi sim ou nao', required=True)
    parser.add_argument('-t', '--tempo', dest='tempo', help='Tempo sem atividade', required=True)
    options = parser.parse_args()
    return options

def separa(a, tam):
    lista = []
    b = []
    for i, l in enumerate(a):
        if i > 1:
            if i / tam == i // tam:
                lista.append(b)
                b = []
        b.append(l)
    lista.append(b)
    return(lista)

def pegaprocessos(tempo):
    with subprocess.Popen(['who', '-u'], stdout=subprocess.PIPE) as proc:
        a = proc.stdout.read().decode('utf-8').split()
    li = separa(a, 7)
    li.sort(key=itemgetter(4))
    lista=[]
    for l in li:
        if len(l[4]) > 2:
            if l[4] == 'antigo':
               lista.append(l)
            else:
                t = int(l[4][:2]) * 60 + int(l[4][-2:])
                if t > tempo:
                   lista.append(l) 
    return(lista)

def pegasubprocessos(lista):
    slista = []
    for l in lista:
        with subprocess.Popen(['ps', '-t', l[1]], stdout=subprocess.PIPE) as proc:
            a = proc.stdout.read().decode('utf-8').split()

        li = separa(a, 4)
        slista.append('Usuario {} => {}'.format(l[0], l[4]))
#        print('Usuario {} => {}'.format(l[0], l[4]))
        for l in reversed(li):
            if l[0] != 'PID':
#                print(l)
                slista.append(l)
    return(slista)

options = get_arguments()

kill = options.simnao.lower()
if kill == 'sim':
    if os.getuid() != 0:
        print('Must be root to run this program!')
        exit(-1)

if not isTime(options.tempo):
    print('Precisa ser uma hora valida, exemplo: 01:45')
    exit(-1)
    
tempo = int(options.tempo[:2]) * 60 + int(options.tempo[-2:])

lista = pegaprocessos(tempo)
slista = pegasubprocessos(lista)

# print(slista)
conta = 0 
for l in slista:
    if isinstance(l, str):
        conta += 1
        print(l)
    else:
        if kill == 'sim':
            subprocess.Popen(['kill', '-9', l[0]], stdout=subprocess.PIPE)
            print(l[0]+' '+l[1]+' '+l[3]+' ==> morto!')
        else:
            print(l[0]+' '+l[1]+' '+l[3])

print('\nNumero de usuarios {}.'.format(conta))
