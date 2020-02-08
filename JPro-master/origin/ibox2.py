#====##====##====##====##====#
#====##====##====##====##====#
'''
INVENTORY: 

- The widget display the current inventory held in house 

'''
#====##====##====##====##====#
#====##====##====##====##====#

import sys 
import datetime
from PyQt5.QtWidgets import (QApplication, 
															QWidget, 
															QSizePolicy,
															QVBoxLayout,
															QHBoxLayout,
															QTableWidget,
															QTableWidgetItem,
															QHeaderView,
															QAbstractItemView,
															)
from connect import Connect 
from dbcreation import Models 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class IBox(QWidget): 

	def __init__(self): 
		super().__init__()

		self.connect = Connect()
		self.all_stock = self.connect.session.query(Models).all()

		self.setGeometry(0,0,640,440)
		self.setWindowTitle('JPro')
#		self.setStyleSheet('background-color: #444444')

		self.buildTable()
		self.setData(self.all_stock)

		self.bargraph = PlotCanvas(self, self.connect, width=4, height=3)
		self.bargraph.move(0,0)

		iboxlayout = QHBoxLayout()
		iboxlayout.addWidget(self.table)
		iboxlayout.addWidget(self.bargraph)	
		self.setLayout(iboxlayout)

		self.show()

	def setData(self, data):
		row = 0 
		for record in data: 
			self.table.setItem(row, 0, QTableWidgetItem(str(record.name)))
			self.table.setItem(row, 1, QTableWidgetItem(str(record.current_quantity)))
#			self.table.setItem(row, 2, QTableWidgetItem(record.parts))
			row += 1 

	def buildTable(self):
		self.table = QTableWidget(len(self.all_stock),2,self)
		self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Models / 模型 '))
		self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Quantity ／ 数量 '))	
#		self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Parts ／ 零件')) 

		self.order_header = self.table.horizontalHeader()
		self.order_header.setMinimumSectionSize(130)
		self.order_header.setSectionResizeMode(QHeaderView.Stretch)

		self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setCurrentCell(-1,-1)

#====##====##====##====##====#
#matplotlib bar chart widget 
#====##====##====##====##====# 
class PlotCanvas(FigureCanvas): 

	def __init__(self, parent, connect, width=5,height=4,dpi=100):
		
		self.fig, self.axes = plt.subplots(figsize=(6,4))
		
		FigureCanvas.__init__(self,self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.plot(connect)

	def plot(self, connect): 
	
		models = [i.name for i in connect.session.query(Models).all()]
		quantity = [i.current_quantity for i in connect.session.query(Models).all()]
		x = np.arange(len(models))

		self.axes.bar(x,quantity, align='center', alpha=0.5, color='lightblue')
		plt.xticks(x,models)
		plt.ylabel('Stock')
		plt.title('Inventory')
		self.axes.margins(0.05)
		self.axes.set_ylim(bottom=0)
		self.fig.set_size_inches(3,4,forward=True)
		#plt.draw()


if __name__ == '__main__' : 

	app = QApplication(sys.argv)
	ibox = IBox()
	sys.exit(app.exec_())