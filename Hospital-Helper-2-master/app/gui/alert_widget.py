import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

from app.gui import utils


class AlertWidget(QFrame):

    """
    Wrapper for AlertWidgetContent.
    Shadows the application.
    """

    def __init__(self, main_window, text, callback=None):
        super().__init__(main_window)
        self.setFixedSize(main_window.size())
        self.show()
        self.move(self.x(), main_window.top_system_frame_height)
        self.raise_()
        AlertWidgetContent(self, main_window, text, callback)


class AlertWidgetContent(QFrame):

    def __init__(self, parent, main_window, text, callback=None):

        """
        Widget for alert messages.
        Also can be user to ask user about something.
        In this case it calls `callback` function with boolean value.
        """

        super().__init__(parent)

        self._close = self._get_close_func(parent, callback)

        vbox = QVBoxLayout()
        l = QLabel(text)
        l.setAlignment(Qt.AlignCenter)
        vbox.addWidget(l)
        vbox.addStretch()

        hbox = QHBoxLayout()
        b = QPushButton('Ok')
        b.clicked.connect(functools.partial(self._close, True))
        hbox.addWidget(b)
        if callback:
            hbox.addStretch()
            # b = QPushButton('Отмена')
            b = QPushButton('Cancelar')
            b.clicked.connect(functools.partial(self._close, False))
            hbox.addWidget(b)

        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()
        self.raise_()
        self.move((main_window.width() - self.width()) / 2, (main_window.height() - self.height()) / 2)
        self.setGraphicsEffect(utils.get_shadow())

    @staticmethod
    def _get_close_func(parent, callback):
        def _close(value):
            if callback:
                callback(value)
            parent.deleteLater()
        return _close
