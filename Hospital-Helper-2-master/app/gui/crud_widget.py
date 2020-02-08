import os
import functools

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QFrame, QLineEdit, QPushButton, QHBoxLayout,
                             QComboBox, QLabel, QVBoxLayout)

from app import options
from app.gui import utils
from app.model import db


class CrudWidget(QFrame):

    """
    Wrapper for CrudWidgetContent.
    Shadows the application.
    """

    def __init__(self, main_window, model, callback=None, item=None):
        super().__init__(main_window)
        self.setFixedSize(main_window.size())
        self.show()
        self.move(self.x(), main_window.top_system_frame_height)
        self.raise_()
        CrudWidgetContent(self, main_window, model, callback, item)


class CrudWidgetContent(QFrame):

    def __init__(self, parent, main_window, model, callback, item=None):

        """
        Widget for CRUD operations on model instances.
        """

        super().__init__(parent)

        self.callback = callback
        self.values = {}
        self.foreigns = {}
        self.model = model
        self.item = item
        self.created_items = []
        self._close = self._get_close_function(parent)
        self._delete = self._get_delete_functon(main_window)

        self._create_layout(main_window)
        self._check_input()

    def _get_controls_layout(self, layout):
        """
        Return buttons layout
        """

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(10)

        # args = ((' Сохранить', ' Закрыть'),
        #         ('save', 'close'),
        #         ('save_w.png', 'close.png'),
        #         (self._save, self._close))

        args = ((' Salvar', ' Fechar'),
                ('save', 'close'),
                ('save_w.png', 'close.png'),
                (self._save, self._close))

        for l, n, i, f in zip(*args):
            b = QPushButton(l)
            b.clicked.connect(f)
            b.setObjectName(n)
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', i)))
            b.setGraphicsEffect(utils.get_shadow())
            hbox.addWidget(b)

        if self.item:
            # b = QPushButton('Удалить')
            b = QPushButton('Excluir')
            b.setObjectName('delete')
            b.clicked.connect(self._delete)
            b.setGraphicsEffect(utils.get_shadow())
            hbox.addWidget(b)

        return hbox

    def _create_layout(self, main_window):
        """
        Create main layout of widget.
        """

        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 10, 30, 10)
        layout.setSpacing(0)

        print(self.model.__table__.name)
        l = QLabel(_(self.model.__table__.name))
        l.setText(self.model.__table__.name)
        l.setObjectName('title')
        layout.addWidget(l)

        scrollable = QVBoxLayout()
        for row in self._get_rows(self.model, main_window):
            for w in row:
                scrollable.addWidget(w)

        scrollable = utils.get_scrollable(scrollable)

        controls_layout = self._get_controls_layout(layout)

        layout.addWidget(scrollable)
        layout.addLayout(controls_layout)

        self.show()
        self.raise_()
        self.move((main_window.width() - self.width()) / 2, (main_window.height() - self.height()) / 2)

    def _get_combobox(self, column, relations, main_window):

        """
        Return combobox for foreign fields.
        """

        label = column.name
        print(label)
        if label.endswith('_id'):
            label = label[:-3]
        foreign_model = relations.get(label).mapper.class_
        items = list(db.SESSION.query(foreign_model).filter(foreign_model.deleted == False))
        self.foreigns[column.name] = items
        items_labels = [str(i) for i in items]
        widget = QWidget()
        widget.setStyleSheet('margin:0;')
        combo_box = QComboBox()
        combo_box.addItems(items_labels)
        combo_box.currentIndexChanged.connect(self._check_input)
        combo_box.setObjectName(column.name)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        hbox.addWidget(combo_box, stretch=95)
        for icon, new in zip(('pencil_g.png', 'plus.png'), (False, True)):
            b = QPushButton()
            b.setObjectName('icon')
            b.setIcon(QIcon(os.path.join(options.STATIC_DIR, 'icons', icon)))
            b.clicked.connect(functools.partial(
                self.open_crud, main_window, foreign_model, new, combo_box))
            hbox.addWidget(b, stretch=2)
        widget.setLayout(hbox)
        return label, widget

    def _get_rows(self, model, main_window):
        """
        Default row for a form is QLabel, QLineEdit
        But for foreign fields it's QComboBox
        Maybe later I will add QCalendar for dates and etc.
        """

        for column in model.__table__.columns:
            if column.name == 'id' or column.default:
                continue

            if column.foreign_keys:
                label, widget = self._get_combobox(column, model.__mapper__.relationships, main_window)
            else:
                label = column.name
                widget = QLineEdit()
                widget.textEdited.connect(self._check_input)
                widget.setObjectName(column.name)
                if self.item:
                    widget.setText(getattr(self.item, column.name, ''))

            print(label)
            # yield QLabel(_(label)), widget
            yield QLabel(label), widget

    def _get_delete_functon(self, main_window):
        def _delete_for_real(for_real):
            if not for_real:
                return
            if hasattr(self.item, 'deleted'):
                self.item.deleted = True
                self.item.save()
            else:
                self.item.delete()
            self._close()

        def _delete():
            """
            Delete item.
            """

            # main_window.create_alert(text='Действие не может быть отменено.\nПродолжить?',
            main_window.create_alert(text='A ação não pode ser desfeita.\nContinua?',
                                     callback=_delete_for_real)
        return _delete

    def _get_close_function(self, parent):
        """
        Delete widget.
        """

        def _close():
            self.callback(self.created_items)
            parent.deleteLater()
        return _close

    def _save(self, event=None):
        """
        Save instance.
        """

        kwargs = {}
        for each in self.findChildren(QLineEdit):
            kwargs[each.objectName()] = each.text()

        for each in self.findChildren(QComboBox):
            kwargs[each.objectName()] = self.foreigns[each.objectName()][
                each.currentIndex()].id

        if self.item:
            self.item.update(**kwargs)
        else:
            self.item = self.model(**kwargs)
        self.item.save()
        self.created_items.append(self.item)
        self._close()

    def _check_input(self):
        """
        Disable 'save' button if not all mandatory fields are filled.
        """

        self.findChild(QPushButton, name='save').setDisabled(
            not all([each.text() for each in self.findChildren(QLineEdit)]))

    def _add_foreign_item(self, combo_box, items):
        """
        Add new instance for combobox.
        """

        for item in items:
            created = True
            for i, each in enumerate(self.foreigns[combo_box.objectName()]):
                if each.id == item.id:
                    self.foreigns[combo_box.objectName()][i] = item
                    combo_box.removeItem(i)
                    combo_box.insertItem(i, str(item))
                    combo_box.setCurrentIndex(i)
                    created = False
                    break
            if created:
                self.created_items.append(item)
                combo_box.addItem(str(item))
                self.foreigns[combo_box.objectName()].append(item)
                combo_box.setCurrentIndex(combo_box.count() - 1)

    def open_crud(self, main_window, model, new, combo_box):

        """
        Open another crud window for foreign instance.
        """

        item = None
        if not new:
            index = combo_box.currentIndex()
            if index == -1:
                return
            item = self.foreigns[combo_box.objectName()][index]

        main_window.create_crud_widget(model, functools.partial(self._add_foreign_item, combo_box), item)
