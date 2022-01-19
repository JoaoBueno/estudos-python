from PyQt5.Qt import QApplication
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget, QLineEdit

import sys

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.le_input = QLineEdit(self)

        reg_ex = QRegExp("[0-9]+.?[0-9]{,2}")
        input_validator = QRegExpValidator(reg_ex, self.le_input)
        self.le_input.setValidator(input_validator)

if __name__ == '__main__':
    a = QApplication(sys.argv)

    w = MyWidget()
    w.show()

    a.exec()