import sys
from PyQt5 import QtWidgets, QtCore, QtGui, Qt


class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()

        # we call our function initGui()
        self.initGui()

        self.window.setGeometry(400, 100, 300, 500)
        self.window.setStyleSheet("border: 3px solid #4e4e4e; background-color:#6e6e6e")
        self.window.show()
        sys.exit(self.app.exec_())

    # create a function to initialize the GUI
    def initGui(self):
        self.applyBtn = QtWidgets.QPushButton("Apply", self.window)
        self.applyBtn.setGeometry(170, 420, 120, 30)
        self.applyBtn.setStyleSheet("background-color:#4e4e4e; color:#f7f7f7;")

        self.cancelBtn = QtWidgets.QPushButton("Cancel", self.window)
        self.cancelBtn.setGeometry(10, 420, 120, 30)
        self.cancelBtn.setStyleSheet("background-color:#4e4e4e; color:#f7f7f7")


main = MainWindow()
