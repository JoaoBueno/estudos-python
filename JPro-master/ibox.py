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
															QHeaderView,
															QTableView,
															QAbstractItemView,	
															)
from dbcreation import Models 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery

class IBox(QWidget): 

	def __init__(self): 
		super().__init__()

	#====##====##====##====##====##====##====#
	# QSqlModel connecition 
	#====##====##====##====##====##====##====#

		# self.db = QSqlDatabase.database("ibox")

		self.db = QSqlDatabase.addDatabase("QSQLITE")
		self.db.setDatabaseName("complete.db")
		self.db.open()

		self.inv_model = QSqlTableModel(self, self.db )
		self.inv_model.setTable("models")
		self.inv_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
		self.inv_model.select()

		self.inv_view = QTableView()
		self.inv_view.setModel(self.inv_model)
		self.inv_view.hideColumn(0)
		self.inv_view.hideColumn(2)

		self.order_header = self.inv_view.horizontalHeader()
		self.order_header.setMinimumSectionSize(130)
		self.order_header.setSectionResizeMode(QHeaderView.Stretch)
		self.inv_view.setSelectionBehavior(QAbstractItemView.SelectRows)


		self.bargraph = PlotCanvas(self, width=4, height=3)
		#self.bargraph.move(0,0)

		#====##====##====##====##====#
		#Layout forming & finalization
		#====##====##====##====##====#

		iboxlayout = QHBoxLayout()
		iboxlayout.addWidget(self.inv_view)
		iboxlayout.addWidget(self.bargraph)	
		self.setLayout(iboxlayout)

#		self.setStyleSheet('background-color: #444444')
		self.setWindowTitle('JPro')
		self.setGeometry(0,0,640,440)
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

	def __init__(self, parent, width=5,height=4,dpi=100):
		
		self.fig, self.axes = plt.subplots(figsize=(6,4))
		
		FigureCanvas.__init__(self,self.fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.plot()

	def plot(self): 
		models_list, quantity_list = [], []
		models_q = QSqlQuery("select name from models")
		quantity_query = QSqlQuery("select current_quantity from models")	
		
		# X DATA 
		while models_q.next(): 
			models_list.append(models_q.value(0)) 		

		#Y DATA		
		while quantity_query.next():
			quantity_list.append(quantity_query.value(0)) 

		x = np.arange(len(models_list))
		self.axes.bar(x,quantity_list, align='center', alpha=0.5, color='lightblue')
		plt.xticks(x,models_list)
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