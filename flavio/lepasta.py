#!/usr/bin/python3

import os


lista = []

def monta_lista(pasta):
    for dirpath, dirnames, files in os.walk(pasta):
        for name in files:
            path = os.path.join(dirpath, name)
            lista.append(path)

    return lista
    