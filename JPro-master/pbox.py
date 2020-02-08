
#====##====##====##====##====#
#====##====##====##====##====#
'''
PRODUCTION QUEUE: 

- The widget contained inside displays a table of current orders 
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
															QTableView,
															QVBoxLayout,
															QHBoxLayout,
															QPushButton,
															qApp,
															QShortcut,
															QDialog,
															QAbstractItemView,
															QGridLayout,
															QHeaderView,									
															)
from PyQt5.QtGui import QKeySequence
from connect import Connect 
from dbcreation import Base, Models, ProductionQueue
from dialog_new import Dialog as DBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class PBox(QWidget): 

	def __init__(self): 
		super().__init__()

		self.label1 = QLabel('Machine Production',self)

		#====##====##====##====##====#
		#SESSION EXTRACTION TO TABLE 
		#====##====##====##====##====#

		#UNCOMMENT FOR FINAL PRODUCT
		# db = QSqlDatabase.database("pbox")

		#Development product - Please turn on to edit widget alone.

		db = QSqlDatabase.addDatabase("QSQLITE")
		db.setDatabaseName("complete.db")
		db.open()

		#Session instance creation 
		#Extract all orders in the procedure queue

		# self.table.setHorizontalHeaderItem(0, QTableWidgetItem('Order No. ／订单号'))
		# self.table.setHorizontalHeaderItem(1, QTableWidgetItem('Model／型号')) 
		# self.table.setHorizontalHeaderItem(2, QTableWidgetItem('Quantity ／ 数量 '))
		# self.table.setHorizontalHeaderItem(3, QTableWidgetItem('Order Date ／ 订单日期'))

		'''
		Use QHeader Class to resize the tables
		'''


		# Iterating through all records 
		
		# self.setData(self.all_orders)

		self.model = QSqlTableModel(self, db)
		self.model.setTable("productionqueue")
		self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
		self.model.select()

		self.tableview = QTableView()
		self.tableview.setModel(self.model)
		self.tableview.hideColumn(0)

		self.order_header = self.tableview.horizontalHeader()
		self.order_header.setMinimumSectionSize(130)
		self.order_header.setSectionResizeMode(QHeaderView.Stretch)
		self.tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
		#self.tableview.setCurrentCell(-1,-1)

		print(self.tableview.rowAt(1))

		self.select = self.tableview.selectionModel()
		print('Current index: ', self.tableview.selectRow(-1))
		print ('Selected: ',self.select.selectedRows())
		print ('has selection: ', self.select.hasSelection())

		#====##====##====##====##====#
		#CONTROL PANEL 
		#====##====##====##====##====#

		self.btn_neworder = QPushButton('New / 加单', self)
		self.btn_neworder.clicked.connect(self.getDBox)

		self.btn_deleterecord = QPushButton('Delete / 取消', self)
		self.btn_deleterecord.clicked.connect(self.deleteRecord)

		#====##====##====##====##====#
		#Layout forming
		#====##====##====##====##====#		

		self.vBox = QVBoxLayout()

		#Adding tableview into VBoxLayout
		self.tableBox = QGridLayout()
		self.tableBox.addWidget(self.tableview)

		self.controlBox = QHBoxLayout()
		self.controlBox.addWidget(self.btn_neworder)
		self.controlBox.addWidget(self.btn_deleterecord)

		self.vBox.addWidget(self.label1)
		self.vBox.addLayout(self.tableBox)
		self.vBox.addLayout(self.controlBox)

		self.setLayout(self.vBox)

		self.setGeometry(0,0,640,440)
		self.show()

		#====##====##====##====##====#
		#CONTROL PANEL 
		#====##====##====##====##====#

	'''
	getDBox: Brings up the Dialog Box from dialog_new
	'''
	def getDBox(self) : 
		dbox = DBox()
		dbox.exec()
		if dbox.oq_input.text():
			# print ('number of rows: ', self.model.rowCount())
			# print(dbox.new_record)
			self.model.insertRecord(self.model.rowCount(),dbox.new_record)
			self.model.submitAll()
			dbox.new_record = -1


	'''
	deleteRecord: 

	- removes both from the view and the database 

	'''			

	def deleteRecord(self):
		if self.select.hasSelection():
			qmodelindex = self.select.selectedRows()[0]
			row = qmodelindex.row()
			self.model.removeRows(row,1)
			self.model.submitAll()


if __name__ == '__main__' : 

	app = QApplication(sys.argv)
	pbox = PBox()
	sys.exit(app.exec_())