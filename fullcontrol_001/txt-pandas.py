#!/usr/bin/python3

import pandas as pd

col_names = ['empresa', 'refer', 'item', 'seq', 'status', 'especie',
             'serie', 'numero', 'fco', 'usuar', 'ano', 'mes', 'dia',
             'hor', 'min', 'seg', 'dec', 'motivo1', 'motivo2', 'resolu',
             'motivo', 'itemcom', 'progr']

col_widths = [2, 3, 3, 18, 1, 3, 3, 8, 15, 12,
              4, 2, 2, 2, 2, 2, 2, 55, 55, 55, 4, 5, 8]

col_types = ['int', 'str', 'str', 'int', 'str', 'str', 'str', 'int', 'str', 'str', 'int',
             'int', 'int', 'int', 'int', 'int', 'int', 'str', 'str', 'str', 'int', 'int',
             'str']

# read into dataframe
df = pd.read_fwf('lgg', widths=col_widths, names=col_names, dtypes=col_types)

print(df.head())

print(df.info())