import sys
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ds = pd.read_csv('caesb.csv', sep='|', encoding='cp1252')
itens = ds.groupby(by='ITEM')
itemtt = itens['QUANTIDADE','VALOR'].aggregate(np.sum)
print(itemtt)
# print(ds)
# print(ds.skew())
# print(ds.describe())
# print(ds.corr())
# ds['ITEM'].hist(bins=30).plot.bar()
# ds['ITEM'].value_counts().plot.bar()
# plt.show()
