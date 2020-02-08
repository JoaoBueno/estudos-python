import sys
from PyQt5.QtWidgets import (QApplication, 
														 QDialog,
														 QLineEdit,
														 QShortcut,
														 qApp,
														 QLabel,
														 QPushButton,
														 QComboBox,
															)
from PyQt5.QtGui import QKeySequence
from dbcreation import Models
from connect import Connect
from dbcreation import ProductionQueue
from PyQt5.QtSql import QSqlDatabase,QSqlQuery,QSqlRecord, QSqlField
import datetime

class Dialog(QDialog): 

	
	def __init__(self): 
		super().__init__()

		self.initdiagUI()

	def initdiagUI(self):

		exitShortcut = QShortcut(QKeySequence('Ctrl+W'),self, qApp.quit)

	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	# Create local seperate connection to databse
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#

		self.db = QSqlDatabase.database("dialog")

	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	# Create SqlRecord template with predefined fields 
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#

		self.record_template = QSqlRecord()
		self.record_template.insert(0, QSqlField('model'))
		self.record_template.insert(1, QSqlField('order_quantity'))
		self.record_template.insert(2, QSqlField('order_time'))
		self.record_template.insert(3, QSqlField('expected_production'))


	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	# Main widgets 
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#

		label_model = QLabel('Model',self)
		label_model.move(40, 50)

		self.combo = QComboBox(self)
		self.fillcombo()
		self.combo.move(180, 50)

		label_orderquantity = QLabel('Order Quantity',self)
		label_orderquantity.move(40, 100)

		self.oq_input = QLineEdit('',self)
		self.oq_input.move(180, 100)


		self.error_message = QLabel('',self)
		self.error_message.move(180, 130)

		btn_submit = QPushButton('Submit Order', self)
		btn_submit.move(180,150)
		btn_submit.clicked.connect(self.submittodb)

		self.setFixedSize(350,200)
		self.setWindowTitle('Input Dialog')
		self.show()		
		self.new_record = -1

	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#

	#							METHODS													#
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#


	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	#Populate combo box with model names using QSqlQuery and QSqlRecord objects
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	def fillcombo(self):
		q = QSqlQuery("select name from models",self.db)
		self.rec = q.record()
		nameCol = self.rec.indexOf("name")
		print (nameCol)
		while q.next():
			self.combo.addItem(q.value(nameCol))

	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	#Submit input data to the model in database
	#=====#	#=====#	#=====#	#=====#	#=====#	#=====#
	def submittodb(self): 
		#print ('Inside label: ', self.oq_input.text())
		if self.oq_input.text().isdigit():
			self.new_record = QSqlRecord(self.record_template)
			self.new_record.setValue(0, self.combo.currentText())
			self.new_record.setValue(1, self.oq_input.text())
			self.new_record.setValue(2, str(datetime.datetime.now()))
			self.close()
		else: 
			self.error_message.setText('Please enter an integer only')
			self.error_message.adjustSize()
			self.error_message.setStyleSheet("color:red")


if __name__ == '__main__' : 

	app = QApplication(sys.argv)
	dialog = Dialog()
	sys.exit(app.exec_())