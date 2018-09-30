import sys
from PyQt5 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.le = QtWidgets.QLineEdit()
        self.b = QtWidgets.QPushButton('Clear')

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.le)
        v_box.addWidget(self.b)

        self.setLayout(v_box)

        self.setWindowTitle('PyQt5 Lesson 6')

        self.show()


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())
