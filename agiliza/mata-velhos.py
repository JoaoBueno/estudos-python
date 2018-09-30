#!/usr/bin/python3

import sys
import subprocess
import argparse
import re
from operator import itemgetter

def isTime(time):
    """Verifica se é uma Hora válida"""
    if not re.match(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time):
        return(False)
    return(True)

def get_arguments():
    parser = argparse.ArgumentParser(description = 'Mata processos antigos')
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
            t = int(l[4][:2]) * 60 + int(l[4][-2:])
            if t > tempo:
               lista.append(l) 
    return(lista)

def pegasubprocessos(lista):
    for l in lista:
        with subprocess.Popen(['ps', '-t', l[1]], stdout=subprocess.PIPE) as proc:
            a = proc.stdout.read().decode('utf-8').split()

        li = separa(a, 4)
        for l in li.reverse:
            print(l)

options = get_arguments()

if isTime(options.tempo):
    tempo = int(options.tempo[:2]) * 60 + int(options.tempo[-2:])
    lista = pegaprocessos(tempo)
    print(lista)
    pegasubprocessos(lista)

