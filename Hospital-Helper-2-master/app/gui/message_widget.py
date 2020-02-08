from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QTimer
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout

from app.gui import utils


class MessageWidget(QFrame):
    """
    Displays message that disappears after some time.
    """

    RIGHT_MARGIN = 20
    TIMEOUT = 1000

    def __init__(self, main_window):
        super().__init__(main_window)

        self.x_pos = 0
        self.label = self._create_layout_and_get_label(main_window)
        self._animation = self._get_animation(main_window)
        self._show = self._get_show_func(main_window)
        self.timer = self._get_timer()

        main_window.communication.set_message_text.connect(self._show)

    def _create_layout_and_get_label(self, main_window):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(vbox)

        l = QLabel()
        l.setAlignment(Qt.AlignCenter)
        l.setScaledContents(True)
        vbox.addWidget(l)
        self.setGraphicsEffect(utils.get_shadow())
        self.hide()

        w = main_window.width() / 5
        self.setFixedSize(w, w * 0.3)
        self.x_pos = main_window.width() - self.width() - self.RIGHT_MARGIN
        self.move(self.x_pos, main_window.height())

        return l

    def _get_animation(self, main_window):
        animation = {'show': QPropertyAnimation(self, b'pos'),
                     'hide': QPropertyAnimation(self, b'pos')}

        animation['show'].setStartValue(QPoint(self.x_pos, main_window.height()))
        animation['show'].setEndValue(QPoint(self.x_pos, main_window.height() - self.height()))
        animation['show'].setDuration(200)
        animation['show'].finished.connect(self._set_timeout_to_hide)

        animation['hide'].setStartValue(QPoint(self.x_pos, main_window.height() - self.height()))
        animation['hide'].setEndValue(QPoint(self.x_pos, main_window.height()))
        animation['hide'].setDuration(200)
        animation['hide'].finished.connect(self.hide)
        return animation

    def _get_timer(self):
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self._hide)
        return timer

    def _set_timeout_to_hide(self):
        self.timer.stop()
        self.timer.start(self.TIMEOUT)

    def _get_show_func(self, main_window):
        def _show(text):
            self.label.setText(text)
            self.show()
            self.raise_()
            self.setFixedSize(self.label.width(), self.height())
            self.move(main_window.width() - self.width() - self.RIGHT_MARGIN,
                      main_window.height())
            self._animation['show'].start()
        return _show

    def _hide(self):
        self._animation['show'].stop()
        self._animation['hide'].start()
        self.timer.stop()

    def mousePressEvent(self, event):
        self._hide()
