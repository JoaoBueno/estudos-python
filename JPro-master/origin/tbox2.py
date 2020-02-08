
#====##====##====##====##====#
#====##====##====##====##====#
'''
WIKI of all items: 

- Uses a Tree view to display pages for each item and its components 
- Display most optimal time and processes needed to run 
 
'''
#====##====##====##====##====#
#====##====##====##====##====#

import sys 
import datetime
from PyQt5.QtWidgets import (QApplication, 
															QWidget, 
															QLabel, 
															QListView,
															QHBoxLayout,
															QVBoxLayout,
															QGridLayout,
															QShortcut,
															qApp,
															)
from PyQt5.QtGui import QKeySequence,QStandardItem,QStandardItemModel
from connect import Connect 
from dbcreation import Base, Models, ProductionQueue
from dialog_new import Dialog as DBox


class TBox(QWidget): 

	def __init__(self): 
		super().__init__()

		exitShortcut = QShortcut(QKeySequence('Ctrl+W'),self, qApp.quit)
		
		self.connect = Connect()

		self.all_models = self.connect.session.query(Models).all()

		self.labelkey_name = QLabel('Name',self)
		self.labelkey_parts = QLabel('Parts',self)
		self.labelkey_current_quantity = QLabel('Current Quantity', self)

		self.labelval_name = QLabel('Name',self)
		self.labelval_parts = QLabel('Parts',self)
		self.labelval_current_quantity = QLabel('Current Quantity', self)		

		self.showInfo('M1')

		self.list = QListView(self)
		self.list_model = QStandardItemModel(self.list)
		self.createList()

		print('Current index of view: ', self.list.currentIndex())

		self.hboxlayout = QHBoxLayout()
		self.label_grid = QGridLayout()
		self.buildLayout()

		self.show()

	def showInfo(self, queryitem):
		query = self.connect.session.query(Models).filter_by(name=queryitem).one()	
		self.labelval_name.setText(query.name)
		self.labelval_parts.setText(query.parts)
		self.labelval_current_quantity.setText(str(query.current_quantity))

	def createList(self): 
		for model in self.all_models : 
			item = QStandardItem(model.name)
			self.list_model.appendRow(item)
		self.list.setModel(self.list_model)
		self.list.setMinimumSize(150,200)
		self.list.setMaximumSize(150,600)
		self.list.show()

	def buildLayout(self):

		self.label_grid.addWidget(self.labelkey_name, 0,0)
		self.label_grid.addWidget(self.labelkey_parts, 1, 0)
		self.label_grid.addWidget(self.labelkey_current_quantity, 2,0)		
		self.label_grid.addWidget(self.labelval_name, 0,1)
		self.label_grid.addWidget(self.labelval_parts,1,1)
		self.label_grid.addWidget(self.labelval_current_quantity,2,1)

		self.hboxlayout.addWidget(self.list)
		self.hboxlayout.addLayout(self.label_grid)
		self.setLayout(self.hboxlayout)

if __name__ == '__main__' : 

	app = QApplication(sys.argv)
	tbox = TBox()
	sys.exit(app.exec_())