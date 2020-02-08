import functools

from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel)

from app.gui.top_system_buttons import TopSystemButtons
from app.gui.select_menu import SelectMenu
from app.gui import utils


class TopFrame(QFrame):

    """
    Top Frame with decorative elements
    """

    def __init__(self, main_window, items):
        super().__init__()

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        top_system_buttons = TopSystemButtons(main_window)
        vbox.addWidget(top_system_buttons)
        vbox.addStretch()
        hbox = QHBoxLayout()
        hbox.addSpacing(25)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(hbox)

        l = QLabel()
        hbox.addWidget(l)
        vbox.addStretch()
        vbox.addWidget(SelectMenu(main_window, items))

        main_window.communication.input_changed_signal.connect(l.setText)
        self.resizeEvent = functools.partial(main_window.resized, self, top_system_buttons)

        self.setGraphicsEffect(utils.get_shadow())
