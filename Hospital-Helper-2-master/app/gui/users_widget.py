import functools

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QLabel, QRadioButton,
                             QHBoxLayout)

from app.model import db
from app.gui import utils


class UsersWidget(QFrame):

    """
    Widget for selecting and creating Users.
    """

    ACTION_BTN_ICON = 'check'

    def __init__(self, main_window):

        super().__init__()

        self.main_window = main_window

        self.content_layout = QVBoxLayout()
        self._update_content()

        vbox = QVBoxLayout()
        vbox.addWidget(utils.get_scrollable(self.content_layout))

        hbox = QHBoxLayout()
        hbox.addStretch(25)
        hbox.addLayout(vbox, stretch=50)
        hbox.addStretch(25)
        self.setLayout(hbox)
        self.showEvent = self._get_show_event(main_window)
        self.setGraphicsEffect(utils.get_shadow())

    def _get_show_event(self, main_window):
        def _show_event(event=None):
            main_window.communication.action_button_toggle.emit(True,
                                                                'plus',
                                                                functools.partial(main_window.create_crud_widget,
                                                                                  db.User,
                                                                                  self._update_content))
        return _show_event

    def _update_content(self, *args):
        """
        If new user or organization were created, update content.
        """

        utils.clear_layout(self.content_layout)
        self.users = list(db.SESSION.query(db.User).filter(db.User.deleted == False,
                                                           db.Organization.deleted == False))
        organizations = list(db.SESSION.query(db.Organization).filter(db.Organization.deleted == False))

        for organization in organizations:
            self.content_layout.addWidget(self._get_label(organization))
            for user in self.users:
                if user.organization_id == organization.id:
                    self.content_layout.addWidget(self._get_radio_btn(user))

        if not self.users:
            # l = QLabel('Создайте пользователей\nдля начала работы')
            l = QLabel('Crie usuários\npara começar')
            l.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(l)
        self.content_layout.addStretch()

    def _get_radio_btn(self, item):
        fullname = '{} {} {}'.format(item.surname, item.name, item.patronymic)
        b = QRadioButton(fullname)
        b.mouseDoubleClickEvent = (functools.partial(self._button_clicked, item))
        return b

    @staticmethod
    def _get_label(item):
        """
        Add label for organization.
        """
        l = QLabel(item.name)
        l.setObjectName(str(item.id))
        return l

    def _button_clicked(self, user, event):
        """
        Select user.
        """
        self.main_window.user_selected(user, go_to_data_frame=True)

