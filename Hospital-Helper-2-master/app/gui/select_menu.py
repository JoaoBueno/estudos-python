import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QFrame,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QGridLayout,
)

from app import options

from app.gui import utils


class SelectMenu(QWidget):

    BUTTON_SELECTED_QSS = "color: white; padding-bottom: 23px; border-bottom: 2px solid #FFEB3B;"

    """
    Line of buttons on TopFrame.
    Used to navigate between frames and items on DataFrame.
    """

    def __init__(self, main_window, items):

        """
        Connects to menu_btn_clicked signal
        and also emits it when button is clicked.
        """

        super().__init__()
        self.hide()

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)
        hbox.addSpacing(25)

        main_window.communication.user_selected.connect(self._show)
        main_window.communication.menu_btn_clicked.connect(self._item_selected)

        self.buttons = []
        labels = [each['sys'] for each in options.CONTROL_BUTTONS_LABELS]

        for i, text in enumerate(labels):
            btn = QPushButton(_(text))
            self.buttons.append(btn)
            if i == 0:
                btn.setStyleSheet(self.BUTTON_SELECTED_QSS)

            btn.clicked.connect(functools.partial(main_window.communication.menu_btn_clicked.emit, i))
            hbox.addWidget(btn)

        SelectItemMenu(main_window, self, items)
        self.buttons[0].setText(_(main_window.items[0].name))
        self.buttons[0].setFixedWidth(int(main_window.width() / 5))
        hbox.addStretch()

    def _item_selected(self, index):
        """
        Change style of selected button.
        """

        for each in self.buttons:
            each.setStyleSheet('')

        self.buttons[index].setStyleSheet(self.BUTTON_SELECTED_QSS)

    def _show(self, *args):
        self.show()
        self.raise_()

    def set_item_label(self, text):
        """
        Change label of button that holds items.
        """

        self.buttons[0].setText(_(text))


class SelectItemMenu(QFrame):

    """
    Float frame.
    Holds names of items.
    Used for navigation.
    Opens on Ctrl key when DataFrame is visible.
    Shows shortcuts to fast switching between items.
    """

    def __init__(self, main_window, select_menu, items):

        super().__init__(main_window)

        self.HINTS = self._get_hints_list()
        self.items = items
        self.resize(main_window.width() * 0.6, main_window.height() * 0.4)
        self.hide()

        main_window.communication.toggle_select_item.connect(self.toggle_visibility)
        main_window.communication.set_select_item_visibility.connect(self.set_visible)
        main_window.communication.ctrl_hotkey.connect(self._show_with_hints)
        main_window.communication.resized.connect(self._move)
        main_window.communication.shortcut_pressed.connect(self._select_for_shortcut)

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        self._btn_clicked_func = self._get_btn_clicked_func(main_window, select_menu)

        cols = 3
        self.hints_labels = []
        for i, item in enumerate(items):
            row, col = i // cols, i % cols
            b = QPushButton(_(item.name))
            b.clicked.connect(functools.partial(self._btn_clicked_func, i))
            grid.addWidget(b, row, col)

            print(self.HINTS[i][0])
            l = QLabel(self.HINTS[i][0], self)
            l.setAlignment(Qt.AlignCenter)
            l.hide()
            self.hints_labels.append(l)

        self.setGraphicsEffect(utils.get_shadow())

    def _move(self, width, waterline, top_sys_btns_height):
        """
        Move to the border between TopFrame and DataFrame.
        """
        self.move(20, waterline)

    def _get_hints_list(self):
        """
        Returns list of keys to show near item labels.
        """

        return [(key, getattr(Qt, 'Key_{}'.format(key), -1))
                for key in '12345qwertsdfgcv'.upper()]

    def _get_btn_clicked_func(self, main_window, select_menu):

        """
        Emit signal when item is selected.
        """

        def _btn_clicked(index):
            select_menu.set_item_label(_(self.items[index].name))
            main_window.communication.item_selected.emit(index)
            self.hide()

        return _btn_clicked

    def toggle_visibility(self):
        self.setVisible(self.isHidden())
        self.raise_()

    def set_visible(self, value):
        self.setVisible(value)
        self.raise_()

    def leaveEvent(self, event):
        self.hide()

    def _show_with_hints(self, is_visible):
        """
        Calls when Ctrl is pressed on DataWidget.
        Show widget with hints.
        """

        for i, item in enumerate(zip(self.hints_labels, self.findChildren(QPushButton))):
            x = item[1].x() + item[1].width() - 80
            item[0].move(x, item[1].y())
            if is_visible:
                item[0].show()
            else:
                item[0].hide()
            self.set_visible(is_visible)

    def _select_for_shortcut(self, key):
        """
        If shortcut is valid imitates button click on required item.
        """

        index = self._get_item_index_by_key(key)
        if index is not None:
            self._btn_clicked_func(index)

    def _get_item_index_by_key(self, key):
        """
        Return index of item by the given shortcut key.
        """

        for i, hint in enumerate(self.HINTS):
            if hint[0] == key:
                return i
