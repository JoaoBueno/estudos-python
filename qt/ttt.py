from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Field(QLabel):
    def __init__(self, text="0", parent=None):
        super(Field, self).__init__(parent=parent)
        self.setAlignment(Qt.AlignCenter)
        self.setText(text)


class IOPanel(QWidget):
    numbers_of_fields = 4
    def __init__(self, parent=None):
        super(IOPanel, self).__init__(parent=None)
        lay = QVBoxLayout(self)
        for _ in range(self.numbers_of_fields):
            w = Field()
            lay.addWidget(w)

        self.setMinimumSize(QSize(40, 0))
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.setSizePolicy(sizePolicy)



class Panel(QWidget):
    def __init__(self, parent=None):
        super(Panel, self).__init__(parent=None)
        lay = QHBoxLayout(self)
        self.input = IOPanel()
        self.output = IOPanel()
        self.canvas = QWidget()

        lay.addWidget(self.input, 0, Qt.AlignLeft)
        lay.addWidget(self.canvas, 0, Qt.AlignCenter)
        lay.addWidget(self.output, 0, Qt.AlignRight)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.initUi()
        self.reset_placement()

    def initUi(self):
        panel = Panel(self)
        self.setCentralWidget(panel)
        self.addToolBar(Qt.BottomToolBarArea, QToolBar(self))

    def reset_placement(self):
        g = QDesktopWidget().availableGeometry()
        self.resize(0.4 * g.width(), 0.4 * g.height())
        self.move(g.center().x() - self.width() / 2, g.center().y() - self.height() / 2)


def main():
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()