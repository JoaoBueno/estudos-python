#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt

# dataset = pd.read_csv('pda_unidades_rf_epct_csv.csv', sep=',')
dataset = pd.read_csv('pda_unidades_rf_epct_csv.csv', sep=';', encoding='cp1252')
# print(type(dataset))
# print(dataset.head())
# print(dataset.columns)
# print(dataset.count())

# print(dataset['NOME_REGIAO_UNIDADE'].value_counts())
# print(dataset['SIGLA_UF_UNIDADE'].value_counts())

# dataset['SIGLA_UF_UNIDADE'].value_counts().plot.bar()
dataset['SIGLA_UF_UNIDADE'].value_counts().plot.pie()
plt.show()
