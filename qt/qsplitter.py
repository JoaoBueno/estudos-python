from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QFrame, QLineEdit, QHBoxLayout, QSplitter
import sys
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 Splitter"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        # self.setWindowFlags(Qt.FramelessWindowHint)
        hbox = QHBoxLayout()
        left = QFrame()
        left.setFrameShape(QFrame.StyledPanel)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.StyledPanel)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.setStyleSheet('background-color:red')
        lineedit = QLineEdit()
        lineedit.setStyleSheet('background-color:green')
        splitter1.addWidget(left)
        splitter1.addWidget(lineedit)
        splitter1.setSizes([200, 200])
        spliiter2 = QSplitter(Qt.Vertical)
        spliiter2.addWidget(splitter1)
        spliiter2.addWidget(bottom)
        spliiter2.setStyleSheet('background-color:yellow')
        hbox.addWidget(spliiter2)
        self.setLayout(hbox)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
