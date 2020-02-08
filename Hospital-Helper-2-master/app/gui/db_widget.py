import os
import math
import functools

from sqlalchemy import sql

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                             QLabel, QGridLayout, QPushButton, QSizePolicy,
                             QLineEdit)

from app import options
from app.model import db, report

from app.gui import utils


class DBWidget(QFrame):

    ITEMS_PER_PAGE = 50

    def __init__(self, main_window):

        """
        Widget to show Client model.
        """

        super().__init__(main_window)

        self.items = []
        self.current_items_index = 0
        self.model = db.Client
        self._query = db.SESSION.query(self.model).order_by(self.model.id.desc())
        self._open_report = self._get_open_report_func(main_window)
        self._delete_item = self._get_delete_item_func(main_window)
        self.columns = []
        self._columns_to_display = ['fullname', 'user', 'age', 'examined', 'controls']
        self.layout = QGridLayout()
        self.header_layout = QGridLayout()
        self.control_layout = QWidget()
        self._page_count_label = QLabel('')
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.addLayout(self._get_search_layout())
        vbox.addLayout(self.header_layout)
        vbox.addWidget(utils.get_scrollable(self.layout))
        vbox.addWidget(self.control_layout)
        self.setLayout(vbox)

        control_layout = QHBoxLayout()
        control_layout.addStretch()
        control_layout.addWidget(self._page_count_label)
        for icon, direciton in zip(('left.png', 'right.png'), (-1, 1)):
            b = QPushButton()
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', icon)))
            b.clicked.connect(functools.partial(self._move, direciton))
            b.setObjectName(icon)
            control_layout.addWidget(b)
        self.control_layout.setLayout(control_layout)
        self.setGraphicsEffect(utils.get_shadow())

        self.showEvent = self._get_show_event(main_window)

    def _get_search_layout(self):
        hbox = QHBoxLayout()
        _input = QLineEdit()
        _input.setGraphicsEffect(utils.get_shadow())
        # _input.setPlaceholderText('Поиск...')
        _input.setPlaceholderText('Pesquisar...')
        _input.textEdited.connect(self._filter)
        hbox.addWidget(_input)
        return hbox

    def _filter(self, query_text):
        # Since it's not really important,
        # I'll keep columns hard-coded here.
        # Sqlalchemy doesn't care about ilike function at all
        if query_text and len(query_text) < 3:
            utils.clear_layout(self.layout)
            # self.layout.addWidget(QLabel('Продолжайте печатать...'))
            self.layout.addWidget(QLabel('Continue digitando...'))
            return
        if query_text:
            query_text = '%{}%'.format(query_text.lower())
            db.cursor.execute(options.SEARCH_QUERY, [query_text, query_text, query_text])
            ids = [i[0] for i in db.cursor.fetchall()]
            if ids:
                self.items = db.SESSION.query(self.model).filter(self.model.id.in_(ids))
            else:
                self.items = db.SESSION.query(self.model).filter(sql.false())
        else:
            self.items = self._query
        self.display_model()

    def _get_show_event(self, main_window):
        def showEvent(event):
            """
            Data is being refreshed on each show.
            """

            if not self.items:
                self.items = self._query

            self.display_model()
            main_window.communication.action_button_toggle.emit(False, '', None)

        return showEvent

    def hideEvent(self, event):
        """
        Delete db items.
        """

        self.items = None

    def display_model(self):
        """
        Clear widget and display items.
        """

        utils.clear_layout(self.layout)

        self.columns = []
        j = 0

        for c in self._columns_to_display:
            self.columns.append(c)
            l = QLabel(_(c))
            l.setObjectName('header')
            l.setAlignment(Qt.AlignCenter)
            self.header_layout.addWidget(l, 0, j)
            j += 1

        for i, item in enumerate(self.items[self.current_items_index:self.current_items_index + self.ITEMS_PER_PAGE]):
            self._add_row(i, item)

        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.layout.addWidget(empty, self.layout.rowCount(), 0)

        if self.current_items_index and self.current_items_index >= self.items.count():
            self.current_items_index = 0
            return self.display_model()

        self.control_layout.setVisible(self.items.count() > self.ITEMS_PER_PAGE)
        page = round(self.current_items_index / self.ITEMS_PER_PAGE) + 1
        page_count = math.floor((self.items.count() - 1) / self.ITEMS_PER_PAGE) + 1
        self._page_count_label.setText('{}/{}'.format(page, page_count))

    def _move(self, direction):
        """
        Navigate between pages.
        """

        index = max(self.current_items_index + self.ITEMS_PER_PAGE * direction, 0)
        if index >= self.items.count():
            return

        self.current_items_index = index
        self.display_model()

    def _get_delete_item_func(self, main_window):
        def _delete_item(item, for_real):
            if not for_real:
                return
            for r in item.report:
                r.delete()
            item.delete()
            self.showEvent(event=None)
            # main_window.show_message('Отчет удален')
            main_window.show_message('Relatório excluído')

        def _ask_before_deletion(item):
            # main_window.create_alert('{} {} {}: удалить отчет?'.format(item.surname, item.name, item.patronymic),
            main_window.create_alert('{} {} {}: Excluir relatório?'.format(item.surname, item.name, item.patronymic),
                                     functools.partial(_delete_item, item))
        return _ask_before_deletion

    @staticmethod
    def _get_open_report_func(main_window):
        def _open_report(item):
            try:
                report.Report.open(item.report[0].path)
            except (IndexError, AttributeError, FileNotFoundError):
                # main_window.create_alert('Не удалось открыть отчет')
                main_window.create_alert('Não foi possível abrir o relatório')
        return _open_report

    def _get_controls_column(self, item):
        layout = QHBoxLayout()
        for i, callback in zip(('open.png', 'delete_g.png'), (self._open_report, self._delete_item)):
            b = QPushButton()
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', i)))
            b.clicked.connect(functools.partial(callback, item))
            layout.addWidget(b)
        return layout

    def _add_row(self, row_id, client):
        """
        Create row for item.
        """
        for j, c in enumerate(self.columns):
            if c == 'controls':
                self.layout.addLayout(self._get_controls_column(client), row_id, j)
                continue
            if c == 'fullname':
                s = '{} {} {}'.format(client.surname, client.name, client.patronymic)
            else:
                s = str(getattr(client, c))
            self.layout.addWidget(QLabel(s), row_id, j)
