import os
import pandas as pd
from leComissao import procComissao
from leFinanc import procFinanc

arqC = 'b-co.ori'
arqF = 'b-fi-v.ori'

arqC = (os.path.splitext(os.path.basename(arqC))[0])
arqF = (os.path.splitext(os.path.basename(arqF))[0])

dfC = procComissao(arqC)
dfF = procFinanc(arqF)

print(dfC.head())
# print(dfC.dtypes)

print(dfF.head())
# print(dfF.dtypes)
