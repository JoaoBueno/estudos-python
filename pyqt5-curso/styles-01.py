#here we import necessary things we need
import sys
from PyQt5 import QtWidgets, QtGui, QtCore, Qt


class MainWindow:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.imagePath = "/home/ily19/Downloads/man (1).png"

        self.initGUI()

        self.window.setWindowTitle("Create a window")
        self.window.setStyleSheet("background-color:#6e6e6e")
        self.window.setGeometry(500, 100, 300,600)
        self.window.show()
        sys.exit(self.app.exec_())

    def initGUI(self):

        #create a label
        self.image = QtGui.QImage(self.imagePath)
        self.label = QtWidgets.QLabel(self.window)
        self.label.setGeometry(50,20, 200,200)
        self.label.setStyleSheet("background-color:#6e6e6e")
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
        self.label.setScaledContents(True)

        #create a pseudo field
        self.pseudo = QtWidgets.QTextEdit(self.window)
        self.pseudo.setGeometry(25,270,250,40)
        self.pseudo.setText("Pseudo")
        self.pseudo.setStyleSheet("background-color:#f7f7f7; color:#8e8e8e; padding-top: 5px; font-size:15px; padding-left:10px")

        #create an email field
        self.email = QtWidgets.QTextEdit(self.window)
        self.email.setGeometry(25, 330,250,40)
        self.email.setText("Email")
        self.email.setStyleSheet("background-color:#f7f7f7; color:#8e8e8e; padding-top: 5px; font-size:15px; padding-left:10px")

        #create a password field
        self.password = QtWidgets.QTextEdit(self.window)
        self.password.setGeometry(25,390,250,40)
        self.password.setText("Password")
        self.password.setStyleSheet("background-color:#f7f7f7; color:#8e8e8e; padding-top: 5px; font-size:15px; padding-left:10px")

        #create a comfirm password field
        self.confirmPassword = QtWidgets.QTextEdit(self.window)
        self.confirmPassword.setGeometry(25,450,250,40)
        self.confirmPassword.setText("Confirm Password")
        self.confirmPassword.setStyleSheet("background-color:#f7f7f7; color:#8e8e8e; padding-top: 5px; font-size:15px; padding-left:10px")

        #creata the create account button
        self.createBtn = QtWidgets.QPushButton(self.window)
        self.createBtn.setText("Create an Account")
        self.createBtn.setGeometry(25, 510, 250, 40)
        self.createBtn.setStyleSheet("background-color:#4e4e4e; color:#fafafa;font-size:15px;border:1px solid #4e4e4e")


#let's instantiate an object to the class MainWindow
main = MainWindow()
