import sys
 
from PySide2.QtWidgets import QDialog, QApplication
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QLineEdit, QLabel, QPushButton
 
class Form(QDialog):
    """"""
 
    def __init__(self, parent=None):
        """Constructor"""
        super(Form, self).__init__(parent)
        main_layout = QVBoxLayout()
 
        name_layout = QHBoxLayout()
        lbl = QLabel("Name:")
        self.name = QLineEdit("")
        name_layout.addWidget(lbl)
        name_layout.addWidget(self.name)
        name_layout.setSpacing(20)
 
        add_layout = QHBoxLayout()
        lbl = QLabel("Address:")
        self.address = QLineEdit("")
        add_layout.addWidget(lbl)
        add_layout.addWidget(self.address)
 
        phone_layout = QHBoxLayout()
        self.phone = QLineEdit("")
        phone_layout.addWidget(QLabel("Phone:"))
        phone_layout.addWidget(self.phone)
        phone_layout.setSpacing(18)
 
        button = QPushButton('Submit')
 
        main_layout.addLayout(name_layout, stretch=1)
        main_layout.addLayout(add_layout, stretch=1)
        main_layout.addLayout(phone_layout, stretch=1)
        main_layout.addWidget(button)
        self.setLayout(main_layout)
 
if __name__ == "__main__":
    app = QApplication([])
    form = Form()
    form.show()
    sys.exit(app.exec_())