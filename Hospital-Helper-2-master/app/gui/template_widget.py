import functools

from bs4 import BeautifulSoup

from PyQt5.Qt import QColor, Qt, QBrush, QFont, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QGuiApplication
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QLabel, QStackedLayout,
                             QVBoxLayout, QPushButton, QTextEdit, QWidget,
                             QRadioButton, QLineEdit, QComboBox)

from app.model import template as template_module
from app.model import exceptions

from app.gui import utils
from app.gui.text_edit_with_format_controls import TextEditWithFormatControls


class SyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, items, parent):
        super().__init__(parent)

        self.rules = []
        self.items = items

        brush = QBrush(QColor(69, 160, 163), Qt.SolidPattern)
        self.item_keywords = QTextCharFormat()
        self.item_keywords.setForeground(brush)
        self.item_keywords.setFontWeight(QFont.Bold)

        self.keywords = QTextCharFormat()
        self.keywords.setForeground(brush)

    def set_rules(self, item):
        self.rules = []
        for each in self.items:
            if each.id == item.id:
                format_ = self.item_keywords
            else:
                format_ = self.keywords

            for w in map(_, each.keys()):
                pattern = QRegExp(r"\{%s.%s\}" % (_(each.name), w))
                self.rules.append({'pattern': pattern, 'format': format_})

        self.rehighlight()

    def highlightBlock(self, text):
        for rule in self.rules:
            expression = QRegExp(rule['pattern'])
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule['format'])
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


class TemplateEditingWidget(QFrame):

    """
    Widget for editing the tempate.
    """

    def __init__(self, main_window, items, close_func):

        super().__init__()

        self.items = items
        self.item = None
        self.template = None
        self.name_text_edit = None
        self.template_text_edit = None
        self.conclusion_text_edit = None
        self.controls_layout = QVBoxLayout()
        self._close = close_func
        self.save = self._get_save_func(main_window)
        self.showEvent = self._get_show_event(main_window)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self._get_control_layout(), stretch=20)
        layout.addLayout(self._get_text_layout(), stretch=80)

    def _get_control_layout(self):
        """
        Create static layout.
        """

        widget = QWidget()
        vbox = QVBoxLayout()
        widget.setLayout(vbox)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.template_combo_box = QComboBox()
        self.template_combo_box.currentIndexChanged.connect(self._item_selected)
        vbox.addWidget(self.template_combo_box)

        scrollable_vbox = utils.get_scrollable(self.controls_layout)
        vbox.addWidget(scrollable_vbox, stretch=80)

        buttons_layout = QHBoxLayout()
        vbox.addLayout(buttons_layout, stretch=20)

        # b = QPushButton('Назад')
        b = QPushButton('Voltar')
        b.setObjectName('controls')
        b.clicked.connect(self._close)
        buttons_layout.addWidget(b)

        widget.setGraphicsEffect(utils.get_shadow())
        return widget

    def _get_text_layout(self):
        """
        Create TextEdit widgets.
        """

        layout = QVBoxLayout()
        self.template_edit_widget = TextEditWithFormatControls(self.items, SyntaxHighlighter)
        self.template_text_edit = self.template_edit_widget.template_text_edit
        self.conclusion_text_edit = TextEditWithFormatControls(self.items, SyntaxHighlighter, ['la', 'ca', 'ra'])
        self.name_text_edit = QLineEdit()

        for w, p, s in zip(self._get_all_text_fields(),
                        #    ('Имя', 'Шаблон', 'Заключение'),
                           ('Nome', 'Modelo', 'Conclusão'),
                           (5, 60, 35)):
            w.setPlaceholderText(p)
            w.setGraphicsEffect(utils.get_shadow())
            layout.addWidget(w, stretch=s)

        return layout

    def _get_show_event(self, main_window):
        def showEvent(event):
            main_window.communication.action_button_toggle.emit(True, 'save', self.save)

        return showEvent

    def _get_all_text_fields(self):
        """
        Get all TextEdit fields.
        """

        return self.name_text_edit, self.template_edit_widget, self.conclusion_text_edit

    def _item_selected(self, index):
        self._fill_controls_layout(self.items[index])

    def _fill_controls_layout(self, item):
        keywords = [_(key) for key in item.keys()]
        utils.clear_layout(self.controls_layout)
        for name in keywords:
            b = QPushButton(_(name))
            b.clicked.connect(functools.partial(self.template_text_edit.insert_attribute, item, name))
            self.controls_layout.addWidget(b)

        self.controls_layout.addStretch()
        return keywords

    def _show(self, item, template=None):
        """
        Fill TextEdit fields with template data if it was provided.
        Add menu buttons with item attributes.
        """

        self.template_text_edit.set_rules(item)

        self.item = item
        self.template = template

        for i, each in enumerate(self.items):
            self.template_combo_box.addItem(_(each.name))
            if each.id == item.id:
                self.template_combo_box.setCurrentIndex(i)

        if self.template:
            self.template = template_module.Template.get_from_db(item=self.item,
                                                                 items=self.items,
                                                                 name=self.template.name)
            self.template.body = self.template.get_translated_body()

            for w, t in zip(self._get_all_text_fields(),
                            (self.template.name, self.template.body, self.template.conclusion)):
                try:
                    w.setHtml(t)
                except AttributeError:
                    w.setText(t)
        else:
            for w in self._get_all_text_fields():
                w.setText('')

    def _get_save_func(self, main_window):
        def save(event):
            """
            Save template.
            """

            if not self.template:
                self.template = template_module.Template()
            self.template.item = self.item
            self.template.items = self.items
            self.template.name = self.name_text_edit.text()

            for attr, text_edit in zip(('body', 'conclusion'), (self.template_text_edit, self.conclusion_text_edit)):
                text = ''.join(filter(lambda x: '\n' not in x,
                                      map(str, BeautifulSoup(text_edit.toHtml(), 'html.parser').body.contents)))
                setattr(self.template, attr, text)

            try:
                self.template.render_and_save()
            except exceptions.CannotSaveTemplate:
                # main_window.create_alert('Не удалось сохранить шаблон.\nПоле "Имя" обязательно.')
                main_window.create_alert('Não foi possível salvar o modelo.\nO campo "Nome" é obrigatório.')
            except exceptions.NeedBodyOrConclusion:
                # main_window.create_alert('Необходимо добавить тело или заключение шаблона.')
                main_window.create_alert('É necessário adicionar um corpo ou uma conclusão padrão.')
            else:
                # main_window.show_message('Шаблон сохранен')
                main_window.show_message('Modelo salvo')
        return save


class AbstractTemplateWidget(QFrame):

    """
    TemplateWidget is used in reports and options tab.
    So it needs several common methods and common layout.
    But behavior is different. it should be defined in children classes.
    """

    def __init__(self, main_window, items):
        super().__init__()

        self.items = items
        self.visible_items = []
        self.layout = QStackedLayout()
        self.menu_layout = QVBoxLayout()
        self.templates_layout = QStackedLayout()
        self.showEvent = self._get_show_event(main_window)
        self.menu_wrapper = QVBoxLayout()

        try:
            self.ACTION_BTN_ICON
        except AttributeError:
            self.ACTION_BTN_ICON = ''

        self.setLayout(self.layout)

        self.layout.addWidget(self._get_static_widgets())

    def _get_static_widgets(self):
        """
        Create layout that does not depend on content.
        """

        hbox = QHBoxLayout()
        self.menu_wrapper.addWidget(utils.get_scrollable(self.menu_layout))
        hbox.addLayout(self.menu_wrapper, stretch=30)
        hbox.addLayout(self.templates_layout, stretch=70)
        widget = QWidget()
        widget.setLayout(hbox)
        widget.setGraphicsEffect(utils.get_shadow())
        return widget

    def _iterate_items(self):
        """
        Filter items if they has no values.
        """
        pass

    def hideEvent(self, event):
        """
        Clear menu and templates.
        """

        utils.clear_layout(self.menu_layout)
        utils.clear_layout(self.templates_layout)

    def _get_show_event(self, main_window):
        """
        Update templates list and re-select them.
        """

        def show_event(event):
            utils.clear_layout(self.menu_layout)
            utils.clear_layout(self.templates_layout)

            self.visible_items = self._iterate_items()
            self._show_menu()
            self._show_templates()
            if not self.layout.currentIndex():
                main_window.communication.action_button_toggle.emit(bool(self.visible_items),
                                                                    self.ACTION_BTN_ICON,
                                                                    self.action_btn_function)

        return show_event

    def _show_menu(self):
        """
        Update menu on showEvent.
        """

        for i, item in enumerate(self.visible_items):
            b = QRadioButton(self._get_button_name(item))
            b.setChecked(i == 0)
            b.clicked.connect(functools.partial(self.templates_layout.setCurrentIndex, i))
            b.setObjectName('menu_button')
            self.menu_layout.addWidget(b)

        if not self.visible_items:
            self.menu_layout.addStretch()
            # l = QLabel('Чтобы создать отчет\nначните заполнять данные')
            l = QLabel('Para criar um relatório,\ninicie os dados de preenchimento')
            l.setAlignment(Qt.AlignCenter)
            self.menu_layout.addWidget(l)

        self.menu_layout.addStretch()

    def _show_templates(self):
        """
        Update templates on shoeEvent.
        """

        cols = 3
        templates = template_module.Template.get_all()
        check_templates = []

        for j, item in enumerate(self.visible_items):
            if not templates[item.id]:
                # l = QLabel('Нет шаблонов для данного объекта\nУправлять шаблонами можно на вкладке настроек')
                l = QLabel('Não há modelos para este objeto\nOs modelos de gerenciamento podem estar na guia de configurações')
                l.setAlignment(Qt.AlignCenter)
                self.templates_layout.addWidget(l)
                continue
            layouts = [QVBoxLayout() for _ in range(cols)]
            for i, each in enumerate(templates[item.id]):
                b = QRadioButton(each.name)
                b.setChecked(item.template == each)
                b.clicked.connect(functools.partial(self._template_clicked, j, each))
                if len(templates[item.id]) == 1:
                    check_templates.append((b, j, each))
                b.mouseDoubleClickEvent = functools.partial(self.open_template_edit_widget, j, each)
                layouts[i % cols].addWidget(b)

            wrapper = QHBoxLayout()
            for each in layouts:
                each.addStretch()
                wrapper.addLayout(each, stretch=int(100 / cols))
            self.templates_layout.addWidget(utils.get_scrollable(wrapper))
        for i, each in enumerate(check_templates):
            b, j, template = each
            self._template_clicked(j, template, i == 0)
            b.setChecked(True)


    def _template_selected(self, index, template):

        """
        Change menu item name.
        Add template for the item.
        """

        self.visible_items[index].template = template
        buttons = self.findChildren(QRadioButton, name='menu_button')
        buttons[index].setText(self._get_button_name(self.visible_items[index]))
        for i in range(len(self.visible_items)):
            ind = (i + index) % len(self.visible_items)
            if not self.visible_items[ind].template:
                self.templates_layout.setCurrentIndex(ind)
                buttons[ind].setChecked(True)
                buttons[index].setChecked(False)
                return

    def _get_button_name(self, item):
        pass

    def _double_click(self, index, template, event):
        pass

    def _template_clicked(self, index, template, show_next=False):
        pass

    def action_btn_function(self, event):
        pass

    def open_template_edit_widget(self, index, template, event):
        pass


class TemplateWidgetInOptions(AbstractTemplateWidget):

    """
    Contains menu with the list of items with templates.
    """

    def __init__(self, main_window, items, parent):
        self.ACTION_BTN_ICON = 'plus'
        super().__init__(main_window, items)

        self.template_editing_widget = TemplateEditingWidget(main_window, items, self._close_func)
        self.layout.addWidget(self.template_editing_widget)
        # b = QPushButton('Назад')
        b = QPushButton('Voltar')
        b.setObjectName('controls')
        b.clicked.connect(functools.partial(parent.set_current_index, 0))
        self.menu_wrapper.addWidget(b)

    def _close_func(self):
        self.layout.setCurrentIndex(0)
        self.showEvent(event=None)

    def _iterate_items(self):
        """
        Return all values.
        """
        return self.items

    def _get_button_name(self, item):
        """
        Return item name
        """
        return _(item.name)

    def open_template_edit_widget(self, index, template=None, event=None):
        """
        Open TemplateEditingWidget with or without template.
        """
        self.layout.setCurrentIndex(1)
        self.template_editing_widget._show(self.visible_items[index], template)

    def action_btn_function(self, event):
        self.open_template_edit_widget(self.templates_layout.currentIndex())


class TemplateWidget(AbstractTemplateWidget):

    def __init__(self, main_window, items):
        self.ACTION_BTN_ICON = 'check'
        self.action_btn_function = main_window.create_report
        super().__init__(main_window, items)

    def _iterate_items(self):
        """
        Filter items if they has no values.
        """
        items = []
        for item in self.items:
            for value in item.values():
                if value:
                    items.append(item)
                    break

        return items

    def _get_button_name(self, item):
        """
        Return item name + template name
        """

        if item.template:
            return '{} - {}'.format(_(item.name), item.template.name)

        return _(item.name)

    def _add_template(self):
        pass

    def _template_clicked(self, index, template, select_next=False):
        """
        Set item's template to selected.
        If Ctrl key pressed - find next item without the template and focus on it.
        """

        self.visible_items[index].template = template
        buttons = self.findChildren(QRadioButton, name='menu_button')
        buttons[index].setText(self._get_button_name(self.visible_items[index]))

        if QGuiApplication.keyboardModifiers() != Qt.ControlModifier and not select_next:
            return

        for i in range(len(self.visible_items)):
            ind = (i + index) % len(self.visible_items)
            if not self.visible_items[ind].template:
                self.templates_layout.setCurrentIndex(ind)
                buttons[ind].setChecked(True)
                buttons[index].setChecked(False)
                return

    def keyPressEvent(self, event):
        if QGuiApplication.keyboardModifiers() != Qt.ControlModifier:
            return
        if event.key() == Qt.Key_Return:
            self.action_btn_function(event=None)
