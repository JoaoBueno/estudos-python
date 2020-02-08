import functools

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QStackedLayout,
                             QVBoxLayout, QPushButton, QFileDialog)

from app import options
from app.model import template

from app.gui import utils
from app.gui.template_widget import TemplateWidgetInOptions
from app.gui.users_and_groups_widget import UsersAndGroupsWidget


class OptionsWidget(QWidget):

    """
    Widget holds menu with all options.
    """

    def __init__(self, main_window, items):

        super().__init__()

        self.items = items

        self.layout = QStackedLayout()
        self._switch_user = self._get_switch_user_func(main_window)
        self.setLayout(self.layout)
        self._hide_action_button = lambda: main_window.communication.action_button_toggle.emit(False, '', None)

        self._create_layout(main_window)

    def set_current_index(self, index):
        self.layout.setCurrentIndex(index)
        if not index:
            self._hide_action_button()

    def showEvent(self, event):
        if not self.layout.currentIndex():
            self._hide_action_button()

    def _get_switch_user_func(self, main_window):
        def _switch_user():
            main_window.menu_btn_clicked(main_window.user_frame_index)
            self.layout.setCurrentIndex(0)
        return _switch_user

    def _get_template_import_func(self, main_window):
        func = self._wrap_template_func(template.Template.import_, main_window)

        def _alert_callback(path, value):
            if value:
                func(path[0])

        def _f():
            # path = QFileDialog.getOpenFileName(main_window, 'Выберите файл', options.DATABASE_DIR)
            path = QFileDialog.getOpenFileName(main_window, 'Selecione o arquivo', options.DATABASE_DIR)
            if path:
                # main_window.create_alert('Шаблоны с одинаковыми именами будут перезаписаны.'
                                        #  '\nПродолжить?', functools.partial(_alert_callback, path))
                main_window.create_alert('Padrões com o mesmo nome serão sobrescritos.'
                                         '\nContinua?', functools.partial(_alert_callback, path))
        return _f

    def _get_template_export_func(self, main_window):
        func = self._wrap_template_func(template.Template.export, main_window)

        def _f():
            # path = QFileDialog.getExistingDirectory(main_window, 'Выберите путь', options.DATABASE_DIR)
            path = QFileDialog.getExistingDirectory(main_window, 'Escolha um caminho', options.DATABASE_DIR)
            if path:
                return func(path)
        return _f

    @staticmethod
    def _wrap_template_func(func, main_window):
        def _f(path):
            ok, result = func(path)
            if ok:
                # main_window.show_message('Готово')
                main_window.show_message('Feito')
            else:
                # main_window.create_alert('Произошла ошибка\n{}'.format(result.get('error')))
                main_window.create_alert('Ocorreu um erro\n{}'.format(result.get('error')))
            return ok, result
        return _f

    def _create_layout(self, main_window):

        wrapper = QHBoxLayout()
        self.layout.addWidget(utils.get_scrollable(wrapper))
        rows = 8
        cols = 3
        vboxes = [QVBoxLayout() for _ in range(cols)]

        # widgets = ((TemplateWidgetInOptions(main_window, self.items, self), 'Шаблоны'),
        #            (UsersAndGroupsWidget(main_window, self), 'Пользователи и группы'),
        #            (self._switch_user, 'Сменить пользователя'),
        #            (self._get_template_export_func(main_window), 'Экспортировать шаблоны'),
        #            (self._get_template_import_func(main_window), 'Импортировать шаблоны'))
        widgets = ((TemplateWidgetInOptions(main_window, self.items, self), 'Templates'),
                   (UsersAndGroupsWidget(main_window, self), 'Usuários e Grupos'),
                   (self._switch_user, 'Alterar usuário'),
                   (self._get_template_export_func(main_window), 'Modelos de exportação'),
                   (self._get_template_import_func(main_window), 'Importar modelos'))

        for i, widget in enumerate(widgets):
            b = QPushButton(widget[1])

            if callable(widget[0]):
                b.clicked.connect(widget[0])
            else:
                b.clicked.connect(functools.partial(self.layout.setCurrentIndex, i + 1))
                self.layout.addWidget(widget[0])

            b.setGraphicsEffect(utils.get_shadow())
            vboxes[(i // rows) % cols].addWidget(b)

        for each in vboxes:
            each.addStretch()
            wrapper.addLayout(each, stretch=int(100 / cols))
