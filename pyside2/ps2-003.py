#!/usr/bin/python

import sys
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import Slot


@Slot()
def say_hello():
    print("Button clicked, Hello!")

def btn(texto, func):
    btn = QPushButton(texto)
    btn.clicked.connect(say_hello)
    return btn


# Create the Qt Application
app = QApplication(sys.argv)
# Create a button, connect it and show it
# button = QPushButton("Click me")
# button.clicked.connect(say_hello)
button = btn("Me Clique", say_hello)
butto1 = btn("teste", say_hello)
button.show()
butto1.show()
# Run the main Qt loop
app.exec_()
