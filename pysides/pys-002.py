import sys
from PySide2.QtWidgets import QApplication, QLabel, QLineEdit
from PySide2.QtWidgets import QDialog, QPushButton, QVBoxLayout
 
class Form(QDialog):
    """"""
 
    def __init__(self, parent=None):
        """Constructor"""
        super(Form, self).__init__(parent)
 
        self.edit = QLineEdit("What's up?")
        self.button = QPushButton("Print to stdout")
 
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
 
        self.setLayout(layout)
 
        self.button.clicked.connect(self.greetings)
 
 
    def greetings(self):
        """"""
        text = self.edit.text()
        print('Contents of QLineEdit widget: {}'.format(text))
 
if __name__ == "__main__":
    app = QApplication([])
    form = Form()
    form.show()
    sys.exit(app.exec_())