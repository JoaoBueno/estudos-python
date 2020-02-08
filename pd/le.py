import pandas as pd

df = pd.read_csv('pedidosabertos.txt', sep='|', encoding='cp1252', decimal=",")

df["VALOR"] = [x.replace(".", "") for x in df["VALOR"]]
df["VALOR"] = [x.replace(",", ".") for x in df["VALOR"]]
df['VALOR'] = df['VALOR'].astype(float)

print(df.dtypes)
print(df)

print(sum(df.VALOR))