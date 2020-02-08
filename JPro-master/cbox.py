#====##====##====##====##====#
#====##====##====##====##====#
'''
Calcuator to find out the total process time for one: 
 
'''
#====##====##====##====##====#
#====##====##====##====##====#

import sys 
import datetime
from PyQt5.QtWidgets import (QApplication, 
															QWidget, 
															QLabel, 
															QTableWidget,
															QTableWidgetItem,
															QListWidget,
															QListWidgetItem,
															QHBoxLayout,
															QVBoxLayout,
															QGridLayout,
															QShortcut,
															qApp,
															QComboBox,
															QHeaderView,
															QAbstractItemView,
															)
from PyQt5.QtGui import QKeySequence,QStandardItem,QStandardItemModel
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from connect import Connect 
from dbcreation import Base, Models, ProductionQueue
from dialog_new import Dialog as DBox

dictionary = {'P1': {'X1':12, 'X2':12, 'X3':12},
							'P2': {'X1':4, 'X2': 6, 'X3': 7}, 
							'P3': {'X4':3, 'X5':3,'X6': 3},
							'P4': {'X4':6, 'X5':6, 'X6':4},
							'P5': {'C1':5, 'X3':5, 'X7':8},
							'P6': {'C1':7, 'X2':5, 'X7':8},
							'P7': {'X3':15, 'X4':13, 'X5':18},
							'P8': {'X2':9, 'X4':9, 'X6':10},
							'P9': {'X3':4, 'X6':5, 'X7':5},
							'P10':{'X1':1, 'X2':1, 'X4': 1}
}

dictionary2 = {'P1': [['X1',12],['X2',12],['X3',12]],
							'P2': [['X1',4],['X2',6],['X3',7]], 
							'P3': [['X4',3], ['X5',3],['X6', 3]],
							'P4': [['X4',6], ['X5',6], ['X6',4]],
							'P5': [['C1',5], ['X3',5], ['X7',8]],
							'P6': [['C1',7], ['X2',5], ['X7',8]],
							'P7': [['X3',15], ['X4',13], ['X5',18]],
							'P8': [['X2',9], ['X4',9], ['X6',10]],
							'P9': [['X3',4], ['X6',5], ['X7',5]],
							'P10':[['X1',1], ['X2',1], ['X4',1]]
}

class CBox(QWidget): 

	def __init__(self): 
		super().__init__()
		exitShortcut = QShortcut(QKeySequence('Ctrl+W'),self, qApp.quit)

		self.connect = Connect()
		self.all_models = self.connect.session.query(Models).all()


		self.table = self.table = QTableWidget(5,3,self)
		self.setTableHeaders()

		self.organiseTable()

		self.populate('M1')
		self.createconnections()

		self.table.move(100,100)


		self.createList()
		self.list.currentItemChanged.connect(self.listClicked)



#		print('Current Item :', self.list.currentItem())
		self.positionWidgets()
		self.mainhbox = QHBoxLayout()
		self.mainhbox.addWidget(self.list)
		self.mainhbox.addWidget(self.table)

		self.setLayout(self.mainhbox)

		self.setGeometry(0,0,640,440)
		self.show()

#===#===#===#===#===#===#===#===#===#
#METHODS
#===#===#===#===#===#===#===#===#===#

	'''
	Set the headers for the table.
	'''
	def setTableHeaders(self):
		self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Parts ／零件'))
		self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Time ／ 时'))		
		self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Process ／机器'))

	'''
	This method resizes the table & allows entire rows to be highlight when selected	
	'''
	def organiseTable(self):
		self.order_header = self.table.horizontalHeader()
		self.order_header.setMinimumSectionSize(130)
		self.order_header.setSectionResizeMode(QHeaderView.Stretch)
		#self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.table.setCurrentCell(-1,-1)

	def populate(self,model):
		parts = self.connect.session.query(Models).filter_by(name = model).one()
		parts = parts.parts.split(',')	
		row = 0
		self.comboboxlist = [QComboBox() for _ in range(len(parts))]
		print (self.comboboxlist)
		for p in parts: 
			self.comboboxlist[row] = self.addComboBox(self.comboboxlist[row], p)
			self.table.setItem(row, 0, QTableWidgetItem(p))
			self.table.setItem(row, 1, QTableWidgetItem(str(self.comboboxlist[row].currentData()))) 
			#self.table.setCellWidget(row,2, self.comboboxlist[row])

			row += 1 

	def createconnections(self):
		for i in range(0,len(self.comboboxlist)):
			self.comboboxlist[i].currentIndexChanged.connect(self.time_combo)

	def time_combo(self,parsed):
		print('object:', parsed)
		

	def generatecombo(self, parts):
		pass

	def addComboBox(self, combobox, part):
		for x in dictionary2[part]:
			combobox.addItem(x[0],x[1])
		return combobox

	def showInfo(self, queryitem):
		# query = self.connect.session.query(Models).filter_by(name=queryitem).one()	
		# self.labelval_name.setText(query.name)
		# self.labelval_parts.setText(query.parts)
		# self.labelval_current_quantity.setText(str(query.current_quantity))

		# self.labelval_parts.adjustSize()
		pass

	def createList(self): 
		self.list = QListWidget(self)
		for model in self.all_models: 
			self.list.addItem(QListWidgetItem(model.name))
			self.list.setMinimumSize(150,200)
			self.list.setMaximumSize(150,600)

	def positionWidgets(self):
		pass

	def listClicked(self):
		current_selection = self.list.currentItem().text()
		self.showInfo(current_selection)

if __name__ == '__main__' : 

	app = QApplication(sys.argv)
	cbox = CBox()
	sys.exit(app.exec_())