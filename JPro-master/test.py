import sys
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
															QComboBox,
															)



class CBox(QWidget): 

	def __init__(self): 
		super().__init__()

		self.table = self.table = QTableWidget(5,3,self)

def createconnections(self):
		for i in range(0,len(self.comboboxlist)):
			self.comboboxlist[i].

self.comboboxlist[row].currentIndexChanged.connect(lambda row: self.time_combo(row))
		
#		self.combobox = QComboBox(self)
#		self.move(400,300)

#		self.combobox.addItem('hello','hello')
#		self.combobox.addItem('sad', 'sad')

		self.setGeometry(0,0,640,440)
		self.show()

if __name__ == '__main__' : 

	app = QApplication(sys.argv)
	tbox = CBox()
	sys.exit(app.exec_())