import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel,
                             QLineEdit)

from app.gui import utils


class InputWidget(QFrame):

    """
    Input contains QLabel and QLineEdit.
    Represents single attribute in CalculableObject object.
    Does not show private attributes that starts from '_'
    """

    def __init__(self, parent, main_window, label_text):
        super().__init__()

        # if label_text.startswith('_'):
        #     return

        self.label_text = label_text
        self.input = QLineEdit()

        main_window.communication.clean_items.connect(self.clean)

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        # hbox.addWidget(QLabel(_(label_text)))
        hbox.addWidget(QLabel(label_text))
        hbox.addStretch()

        self.input.setAlignment(Qt.AlignRight)
        # self.input.setFixedWidth(190)
        self.input.textEdited.connect(functools.partial(parent.input_changed, label_text))

        self.setGraphicsEffect(utils.get_shadow())
        hbox.addWidget(self.input)

    def set_value(self, value):
        if value:
            self.input.setText(str(value))

    def clean(self):
        self.input.setText('')

    def mousePressEvent(self, event):
        self.input.setFocus()
