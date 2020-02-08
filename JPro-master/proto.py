import numpy as np 
import matplotlib.pyplot as plt

from connect import Connect
from dbcreation import Models

main = Connect()

models = [i.name for i in main.session.query(Models).all()]
print ('models: ', models)

names = ['M1','M2','M3','M4']
x = np.arange(len(models))

quantity = [100,200,300,150]

def main(): 

	fig, axes = plt.subplots(figsize=(6,4))
	axes.bar(x,quantity, align='center', alpha=0.5, color='lightblue')
	plt.xticks(x,models)
	plt.ylabel('Stock')
	plt.title('Inventory')
	axes.margins(0.05)
	axes.set_ylim(bottom=0)
	plt.show()

main()
