import os
import sys
import functools
import traceback as trb
import datetime

from sqlalchemy.orm import exc

from PyQt5.QtCore import QCoreApplication, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QStackedLayout, QDesktopWidget,
                             QVBoxLayout, QShortcut, QApplication, QSplashScreen)

from PyQt5.QtGui import QKeySequence, QPixmap, QIcon

from app import options
from app.model import db, report

from app.gui.top_frame import TopFrame
from app.gui.users_widget import UsersWidget
from app.gui.data_widget import DataWidget
from app.gui.db_widget import DBWidget
from app.gui.options_widget import OptionsWidget
from app.gui.template_widget import TemplateWidget
from app.gui.action_button import ActionButton
from app.gui.crud_widget import CrudWidget
from app.gui.alert_widget import AlertWidget
from app.gui.message_widget import MessageWidget


class Communication(QObject):
    """
    Object defines signals for application.
    """

    user_selected = pyqtSignal(object)
    menu_btn_clicked = pyqtSignal(int)
    input_changed_signal = pyqtSignal(str)
    resized = pyqtSignal(float, float, float)
    set_select_item_visibility = pyqtSignal(bool)
    item_selected = pyqtSignal(int)
    toggle_select_item = pyqtSignal()
    ctrl_hotkey = pyqtSignal(bool)
    shortcut_pressed = pyqtSignal(str)
    action_button_toggle = pyqtSignal(bool, str, object)
    clean_items = pyqtSignal()
    set_message_text = pyqtSignal(str)


class MainWindow(QWidget):
    """
    Root widget for application.
    Handles signals.
    """

    def __init__(self, items):
        """
        Init gui.
        Connect signals.
        Create layout.
        """

        super().__init__()

        self.items = items
        self.user = None
        self.communication = Communication()
        self.frames_layout = QStackedLayout()
        self.data_frame_index = None
        self.top_system_frame_height = 0

        self._init_gui()
        self._set_shortcuts()

    def _init_gui(self):
        self._set_sys_attributes()
        self._create_layout()
        self.communication.menu_btn_clicked.connect(self.menu_btn_clicked)
        self.show()
        self._first_start_check()

    def _first_start_check(self):

        def _import_templates(value):
            if value:
                from app.model import template
                template.Template.import_(options.INIT_TEMPLATES_PATH)
                # self.show_message('Готово!')
                self.show_message('Feito!')
            db.KeyValue(key=options.FIRST_START_KEY, value='').save()

        try:
            first_time = db.KeyValue.get(key=options.FIRST_START_KEY).value
        except (exc.NoResultFound, AttributeError):
            first_time = True

        if first_time:
            self.create_alert(options.FIRST_START_WELCOME_TEXT, _import_templates)

    def _create_layout(self):
        """
        Add TopFrame and main frames.
        """

        MessageWidget(self)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        self.setLayout(vbox)

        ActionButton(self)
        vbox.addWidget(TopFrame(self, self.items), stretch=15)
        vbox.addLayout(self.frames_layout, stretch=40)
        self._add_frames()
        self.show()

    def _add_frames(self):
        """
        Add frames to stacked layout.
        """

        frames = [
            DataWidget(self, self.items),
            TemplateWidget(self, self.items),
            DBWidget(self),
            OptionsWidget(self, self.items),
            UsersWidget(self),
        ]

        for i, frame in enumerate(frames):
            if isinstance(frame, DataWidget):
                self.data_frame_index = i
            if isinstance(frame, UsersWidget):
                self.user_frame_index = i
            self.frames_layout.addWidget(frame)

        self.frames_layout.setCurrentIndex(len(frames) - 1)

    def _set_sys_attributes(self):
        """
        Set sys attributes like window title.
        Disable OS-specific buttons.
        Remove borders.
        """

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setWindowTitle('Hospital Helper')
        dw = QDesktopWidget()
        w = min(1300, dw.geometry().size().width() * 0.75)
        self.setFixedSize(w, w * 0.65)
        qr = self.frameGeometry()
        cp = dw.availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def menu_btn_clicked(self, index):
        """
        Callback to switch between main frames.
        """

        if self.frames_layout.currentIndex() == index == self.data_frame_index:
            self.communication.toggle_select_item.emit()
            return
        else:
            self.communication.set_select_item_visibility.emit(False)
        self.frames_layout.setCurrentIndex(index)

    def input_changed(self, item):
        """
        Change TopFrame label when client name is changed.
        Emit signal for TopFrame.
        """

        # Well it doesnt look good, but i was never good with UI.
        if self.items.index(item) == 0:
            text = []
            for i, key in enumerate(item.keys()):
                if item[key]:
                    text.append(str(item[key]))
                if i == 2:
                    break

            self.communication.input_changed_signal.emit(' '.join(text))

    def _set_shortcuts(self):
        """
        Set shortcuts for fast items switch on DataWidget.
        """

        def _shortcut_callback(key):
            if self.frames_layout.currentIndex() != self.data_frame_index:
                return
            self.communication.shortcut_pressed.emit(key)

        # QShortcut(QKeySequence('Esc'), self).activated.connect(self.close)
        keys = [str(i) for i in range(0, 11)] + [chr(c) for c in range(ord('A'), ord('Z') + 1)]
        for key in keys:
            QShortcut(QKeySequence('Ctrl+{}'.format(key)), self).activated.connect(
                functools.partial(_shortcut_callback, key))

    def create_crud_widget(self, model, callback, db_object=None):
        """
        Add CrudWidget with self as parent
        """

        CrudWidget(self, model, callback, db_object)

    def create_alert(self, text, callback=None):
        AlertWidget(self, text, callback)

    def show_message(self, text):
        self.communication.set_message_text.emit(text)

    def user_selected(self, user, go_to_data_frame=False):
        """
        Callback when user is selected.
        Sets user, emits signal.
        """

        self.user = user
        self.communication.user_selected.emit(user)
        if go_to_data_frame:
            self.communication.menu_btn_clicked.emit(self.data_frame_index)

    def create_report(self, event=None):
        """
        Render and save report.
        Open report in default OS program.
        """

        r = report.Report(self.user, self.items)
        db_report = r.render_and_save()
        r.open(db_report.path)
        # self.show_message('Отчет создан')
        self.show_message('Relatório criado')

    def clean_input(self):
        def _clean_input(value):
            if not value:
                return

            self.communication.clean_items.emit()
            self.communication.input_changed_signal.emit('')
            for item in self.items:
                item.clean()
            self.show_message('Ok')

        # self.create_alert('Очистить все поля?', _clean_input)
        self.create_alert('Limpar todos os campos?', _clean_input)

    def resized(self, top_frame, top_sys_btns, event):
        """
        Called when window is resized.
        Calculates Y position of the border between TopFrame and DataFrame
        """

        waterline = top_frame.y() + top_frame.height()
        self.top_system_frame_height = top_sys_btns.height()
        self.communication.resized.emit(self.width(), waterline, self.top_system_frame_height)

    def keyPressEvent(self, event):
        """
        If key is Ctrl - toggle SelectItemMenu visibility.
        If key is Ctrl+Return - opens ReportFrame
        Emits signal.
        """

        mods = event.modifiers()
        if mods & Qt.ControlModifier and self.frames_layout.currentIndex() == self.data_frame_index:
            if event.text() is '':
                self.communication.ctrl_hotkey.emit(True)
                return
            elif event.key() == Qt.Key_Return:
                self.communication.menu_btn_clicked.emit(self.data_frame_index + 1)

    def keyReleaseEvent(self, event):
        """
        If key is Ctrl - toggle SelectItemMenu visibility.
        """

        if event.text() is '':
            self.communication.ctrl_hotkey.emit(False)

    def close(self, event=None):
        """
        Close the application
        """

        QCoreApplication.instance().quit()

    def minimize(self, event=None):
        """
        Minimize the application
        """

        self.setWindowState(Qt.WindowMinimized)

    def excepthook(self, exctype, value, traceback):
        with open(options.LOG_FILE, 'a') as f:
            f.write('\n{}\n{}'.format(datetime.datetime.now(),
                                      '\n'.join(trb.format_exception(exctype, value, traceback))))

        # self.create_alert('Произошла непредвиденная ошибка.\n'
        #                   'Попробуйте повторить действие, хотя это вряд ли поможет')
        self.create_alert('Um erro inesperado ocorreu.\n'
                          'Tente repetir a ação, embora seja improvável que isso ajude.')


def init(bootstrap_function):
    """
    Init gui.
    Concat all files from style directory and apply stylesheet.
    Run `bootstrap_function` to prepare app.
    """
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(options.STATIC_DIR, 'splash.png')))
    splash_img = QPixmap(os.path.join(options.STATIC_DIR, 'splash.png'))
    splash = QSplashScreen(splash_img)
    splash.show()
    app.processEvents()

    items = bootstrap_function()

    style = []
    style_dir = os.path.join(options.STATIC_DIR, 'style')
    for f in os.listdir(style_dir):
        if not f.endswith('.qss'):
            continue
        with open(os.path.join(style_dir, f), 'r') as qss:
            style.append(qss.read())
    app.setStyleSheet('\n'.join(style))

    mw = MainWindow(items)
    splash.finish(mw)

    sys.excepthook = mw.excepthook
    sys.exit(app.exec_())
