import os
import functools

from bs4 import BeautifulSoup

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QVBoxLayout, QComboBox,
                             QPushButton, QTextEdit, QWidget)

from app import options
from app.model import db

from app.gui.crud_widget import CrudWidget
from app.gui.text_edit_with_format_controls import TextEditWithFormatControls
from app.gui import utils


class UsersAndGroupsWidget(QFrame):
    """
    Provide the way to add or delete groups and also dit group name and header.
    """

    def __init__(self, main_window, parent):
        super().__init__()

        self._groups_combo_box = None
        self._users_layout = None
        self._text_field = None
        self._related_to_group_buttons = []
        self.show_message = main_window.communication.set_message_text.emit
        self._show_crud = self._get_crud_func(main_window)
        self.showEvent = self._get_show_event(main_window)
        self._delete = self._get_delete_func(main_window)
        self._select_user = self._get_select_user(main_window)
        self.groups = []
        self.users = []
        self._selected_group = None

        self._create_layout(parent)

    def _create_layout(self, parent):
        self._groups_combo_box = QComboBox()
        self._users_layout = QVBoxLayout()
        self._text_field = TextEditWithFormatControls()

        # self._text_field.setPlaceholderText('Заголовок появится в начале отчета')
        self._text_field.setPlaceholderText('Um título aparecerá no início do relatório.')
        self._groups_combo_box.currentIndexChanged.connect(self._group_selected)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)

        right_side = QVBoxLayout()
        right_side.setContentsMargins(0, 0, 0, 0)
        right_side.setSpacing(0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        for i, f in zip(('save_w', 'delete'), (self._save, self._delete)):
            b = QPushButton()
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', i)))
            b.setObjectName('button')
            b.clicked.connect(f)
            hbox.addWidget(b)
            self._related_to_group_buttons.append(b)
            hbox.addSpacing(5)
        hbox.addStretch()
        right_side.addLayout(hbox)
        right_side.addSpacing(5)
        # l = QLabel('Заголовок')
        l = QLabel('Headline')
        l.setObjectName('text-header')
        right_side.addWidget(l)
        right_side.addWidget(self._text_field)

        left_side = QVBoxLayout()
        left_side.setContentsMargins(0, 0, 0, 0)
        left_side.setSpacing(0)
        left_side.addWidget(self._groups_combo_box)
        wrapper = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        # l = QLabel('Пользователи')
        l = QLabel('Usuários')
        l.setObjectName('header')
        hbox.addWidget(l)
        hbox.addStretch()
        b = QPushButton()
        b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', 'plus')))
        b.clicked.connect(functools.partial(self._show_crud, db.User))
        hbox.addWidget(b)
        wrapper.setLayout(hbox)
        wrapper.setObjectName('header')
        left_side.addWidget(wrapper)
        left_side.addWidget(utils.get_scrollable(self._users_layout))
        # b = QPushButton('Назад')
        b = QPushButton('Voltar')
        b.setObjectName('button')
        b.clicked.connect(functools.partial(parent.set_current_index, 0))
        left_side.addSpacing(5)
        left_side.addWidget(b)

        layout.addLayout(left_side, stretch=30)
        layout.addLayout(right_side, stretch=70)
        self.setLayout(layout)
        self.setGraphicsEffect(utils.get_shadow())

    def _get_crud_func(self, main_window):
        def _show_crud(model, item=None):
            CrudWidget(main_window, model=model, callback=self._refresh, item=item)

        return _show_crud

    def _get_show_event(self, main_window):
        def _show_event(event=None):
            main_window.communication.action_button_toggle.emit(True, 'plus', functools.partial(self._show_crud,
                                                                                                db.Organization))
            self._refresh()

        return _show_event

    @staticmethod
    def _get_select_user(main_window):
        def _select_user(user):
            def callback(value):
                if value:
                    main_window.communication.user_selected.emit(user)

            # main_window.create_alert(text='Сменить пользователя?',
            main_window.create_alert(text='Alterar usuário?',
                                     callback=callback)

        return _select_user

    def _show_users_for_group(self, group_id):
        utils.clear_layout(self._users_layout)

        for user in db.SESSION.query(db.User).filter(db.User.organization_id == group_id,
                                                             db.User.deleted == False,
                                                             db.Organization.deleted == False):
            layout = QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            layout.addWidget(QLabel(str(user)))
            layout.addStretch()
            for i, f in zip(('check', 'pencil_g'),
                            (functools.partial(self._select_user, user),
                             functools.partial(self._show_crud, db.User, user))):
                b = QPushButton()
                b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', i)))
                b.clicked.connect(f)
                layout.addWidget(b)
            wrapper = QWidget()
            wrapper.setLayout(layout)
            self._users_layout.addWidget(wrapper)
        self._users_layout.addStretch()

    def _set_buttons_state(self, value):
        for b in self._related_to_group_buttons:
            b.setDisabled(value)

    def _group_selected(self, index):
        try:
            self._selected_group = self.groups[index]
        except IndexError:
            self._text_field.setText('')
            self._set_buttons_state(True)
        else:
            self._show_users_for_group(self._selected_group.id)
            self._set_buttons_state(False)
            self._text_field.setText(self._selected_group.header)

    def _refresh(self, items=None):
        self.groups = list(db.SESSION.query(db.Organization).filter(db.Organization.deleted == False))
        self._clear_layout()

        if not self.groups:
            self._users_layout.addStretch()
            # l = QLabel('Создайте группу, чтобы добавлять пользователей.')
            l = QLabel('Crie um grupo para adicionar usuários.')
            l.setAlignment(Qt.AlignCenter)
            self._users_layout.addWidget(l)
            self._users_layout.addStretch()
            return

        for i, group in enumerate(self.groups):
            if self._selected_group and group.id == self._selected_group.id:
                self._group_selected(i)

            self._groups_combo_box.insertItem(i, str(group))

    def _clear_layout(self):
        utils.clear_layout(self._users_layout)
        self._text_field.setText('')
        for i in range(self._groups_combo_box.count()):
            self._groups_combo_box.removeItem(i)

    def _save(self):

        if not self._selected_group:
            return

        self._selected_group.header = ''.join(filter(lambda x: '\n' not in x,
                                                     map(str, BeautifulSoup(self._text_field.toHtml(),
                                                                            'html.parser').body.contents)))
        self._selected_group.save()
        self.show_message('Ок')

    def _get_delete_func(self, main_window):
        def _delete_for_real(for_real):
            if not for_real:
                return
            self._selected_group.deleted = True
            self._selected_group.save()
            self._selected_group = None
            self._refresh()
            return

        def _delete():
            # main_window.create_alert(text='Действие не может быть отменено.\nПродолжить?', callback=_delete_for_real)
            main_window.create_alert(text='A ação não pode ser desfeita.\nContinua?', callback=_delete_for_real)

        return _delete
