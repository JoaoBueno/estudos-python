
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
															QListWidget,
															QListWidgetItem,
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

		self.labelval_name = QLabel('Model ／ 模型 ',self)
		self.labelkey_parts = QLabel('Parts ／ 零件',self)
		self.labelkey_current_quantity = QLabel('Current Quantity / 数量', self)
		self.labelval_parts = QLabel('N/A',self)
		self.labelval_current_quantity = QLabel('N/A', self)		

		self.createList()
		self.list.currentItemChanged.connect(self.listClicked)

#		print('Current Item :', self.list.currentItem())
		self.positionWidgets()
		self.styling()

		self.setGeometry(0,0,640,440)
		self.show()

#===#===#===#===#===#===#===#===#===#
#METHODS
#===#===#===#===#===#===#===#===#===#
	def showInfo(self, queryitem):
		query = self.connect.session.query(Models).filter_by(name=queryitem).one()	
		self.labelval_name.setText(query.name)
		self.labelval_parts.setText(query.parts)
		self.labelval_current_quantity.setText(str(query.current_quantity))

		self.labelval_parts.adjustSize()

	def createList(self): 
		self.list = QListWidget(self)
		for model in self.all_models: 
			self.list.addItem(QListWidgetItem(model.name))
			self.list.setMinimumSize(150,200)
			self.list.setMaximumSize(150,600)

	def positionWidgets(self):
		self.list.move(10,10)
		self.labelval_name.move(300, 30)
		self.labelkey_parts.move(200, 150)
		self.labelkey_current_quantity.move(200,200)
		self.labelval_parts.move(400,150)
		self.labelval_current_quantity.move(400,200)

	def styling(self):
		self.labelval_name.setStyleSheet('font-size:24px')
		self.labelkey_parts.setStyleSheet('font-size:14px')
		self.labelkey_current_quantity.setStyleSheet('font-size:14px')
		self.labelval_parts.setStyleSheet('font-size:14px')
		self.labelval_current_quantity.setStyleSheet('font-size:14px')

	def listClicked(self):
		current_selection = self.list.currentItem().text()
		self.showInfo(current_selection)

if __name__ == '__main__' : 

	app = QApplication(sys.argv)
	tbox = TBox()
	sys.exit(app.exec_())