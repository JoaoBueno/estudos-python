import sys
from PyQt5 import QtWidgets, QtGui


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    l1 = QtWidgets.QLabel(w)
    l2 = QtWidgets.QLabel(w)
    l1.setText('Hello World')
    l2.setPixmap(QtGui.QPixmap('globe.png'))
    w.setWindowTitle('PyQt5 Lesson 2')
    w.setGeometry(100, 100, 300, 200)
    l1.move(100, 20)
    l2.move(120, 90)
    w.show()
    sys.exit(app.exec_())


window()
