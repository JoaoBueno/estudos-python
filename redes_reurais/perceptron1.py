# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 14:16:04 2017

@author: Jones
"""
entradas = [-1, 7, 5, 6]
pesos = [0.8, 0.1, 0, 0.3]

def soma(e, p):
    s = 0
    for i in range(len(e)):
        #print(entradas[i])
        #print(pesos[i])
        print(e[i]*p[i])
        s += e[i] * p[i]
    return s
        
s = soma(entradas, pesos)
print(s)

def stepFunction(soma):
    if (soma >= 1):
        return 1
    return 0

r = stepFunction(s)
print(r)