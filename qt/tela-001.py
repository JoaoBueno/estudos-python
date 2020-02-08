# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tela-001.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("font: 14pt \"Roboto\";")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.base = QtWidgets.QFrame(self.centralwidget)
        self.base.setStyleSheet("background-color: #282A36;")
        self.base.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.base.setFrameShadow(QtWidgets.QFrame.Raised)
        self.base.setObjectName("base")

        self.menu = QtWidgets.QFrame(self.base)
        # self.menu.setGeometry(QtCore.QRect(0, 0, 340, 600))
        self.menu.setStyleSheet("background-color: #21222C;")
        self.menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.menu.setObjectName("menu")

        self.gridLayout.addWidget(self.base, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.menu, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
