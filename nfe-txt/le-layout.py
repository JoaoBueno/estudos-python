import sys
import csv


def cria_lista(arq):
    lista = []
    with open(arq, newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter="|")
        for linha in spamreader:
            lista.append(linha)
    return lista


def in_list(item, L):
    for i in L:
        if item in i:
            return L.index(i)
    return -1


lista_layout = cria_lista("layout.txt")
lista_nfe = cria_lista("413034_001_001_06_08_2018-nfe.txt")

for l in lista_nfe:
    r = in_list(l[0], lista_layout)
    if r >=0:
        for p in range(len(lista_layout[r])):
            print(lista_layout[r][p], ": ", l[p], end=", ")
        print()
    else:
        print('Elemento não encontrado:', l[0])
