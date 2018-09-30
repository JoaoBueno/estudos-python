#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Регистрируем новых сотрудников
Cadastro de novos funcionários
"""
from app.db import data
from app.tablewidgets.pcsadd import PCAdd
from app.tools.functions import get_or_create
from app.tools.exitmethods import Dialog
from sqlalchemy.sql.operators import exists
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class RegisterEmployee(Dialog):
    def __init__(self, session):
        QDialog.__init__(self)
        self.session = session
        self.added_pcs = []
        self.init_window()
        self.init_layouts()

    def init_window(self):
        self.setFixedWidth(700)
        self.setWindowModality(2)
        self.setWindowTitle('Cadastro de funcionário')
        self.setWindowIcon(QIcon(r'pics\employee.png'))

    def init_layouts(self):
        buttons_layout = QHBoxLayout()

        back_button = QPushButton('Voltar')
        back_button.clicked.connect(self.close)
        submit_button = QPushButton('Adicionar ao banco de dados')
        submit_button.clicked.connect(self.validate_input)
        buttons_layout.addWidget(back_button, alignment=Qt.AlignRight)
        buttons_layout.addWidget(submit_button)

        form_layout = QFormLayout(self)

        self.surname_edit = QLineEdit()
        self.surname_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        self.surname_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Sobrenome:<font color="red">*</font>', self.surname_edit
        )
        self.name_edit = QLineEdit()
        self.name_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        self.name_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Nome:<font color="red">*</font>', self.name_edit
        )
        self.patronymic_edit = QLineEdit()
        self.patronymic_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        self.patronymic_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Nome do meio:', self.patronymic_edit
        )
        self.login_edit = QLineEdit()
        self.login_edit.setValidator(QRegExpValidator(QRegExp("[^ ]+")))
        self.login_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Login:<font color="red">*</font>', self.login_edit
        )
        phone_edit = QLineEdit()
        phone_edit.setInputMask('+55(999)99999-9999;_')
        self.phone_edit = [phone_edit]
        self.add_phone_button = QPushButton('+')
        self.add_phone_button.clicked.connect(self.add_phone)
        self.add_phone_button.setFixedSize(self.add_phone_button.sizeHint())
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(phone_edit)
        phone_layout.addWidget(self.add_phone_button)
        form_layout.addRow(
            'Número de telefone:', phone_layout
        )
        email_edit = QLineEdit()
        self.email_edit = [email_edit]
        self.add_email_button = QPushButton('+')
        self.add_email_button.clicked.connect(self.add_email)
        self.add_email_button.setFixedSize(self.add_email_button.sizeHint())
        email_layout = QHBoxLayout()
        email_layout.addWidget(email_edit)
        email_layout.addWidget(self.add_email_button)
        form_layout.addRow(
            'E-mail:', email_layout
        )
        self.position_edit = QComboBox()
        self.position_edit.setEditable(True)
        self.position_edit.addItems([
            position
            for (position,) in self.session.query(data.Position.name)
            if position
        ])
        self.position_edit.setCurrentText('')
        form_layout.addRow(
            'Posição:', self.position_edit
        )
        self.department_edit = QComboBox()
        self.department_edit.setEditable(True)
        self.department_edit.addItems([
            department
            for (department,) in self.session.query(data.Department.name)
            if department
        ])
        self.department_edit.setCurrentText('')
        form_layout.addRow(
            'Departamento:', self.department_edit
        )
        self.address_edit = QComboBox()
        self.address_edit.addItems(
            self.session.query(data.Address.name).values()
        )
        self.address_edit.currentIndexChanged[str].connect(
            self.changed_item_in_address_combobox
        )
        form_layout.addRow(
            'Endereço:<font color="red">*</font>', self.address_edit
        )
        self.block_edit = QComboBox()
        form_layout.addRow(
            'Habitação:<font color="red">*</font>', self.block_edit
        )
        self.block_edit.addItems(
            self.session.query(data.Block.name). \
                join(data.Address). \
                filter(data.Address.name == self.address_edit.currentText()). \
                values()
        )
        self.room_edit = QLineEdit()
        self.room_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Sala:<font color="red">*</font>', self.room_edit
        )
        self.comments_edit = QLineEdit()
        self.comments_edit.setClearButtonEnabled(True)
        form_layout.addRow(
            'Outro:', self.comments_edit
        )
        self.shared_folder_edit = QCheckBox()
        form_layout.addRow(
            'Pastas compartilhadas:', self.shared_folder_edit
        )
        self.network_printer_edit = QCheckBox()
        form_layout.addRow(
            'Impressora de rede:', self.network_printer_edit
        )

        table_layout = QVBoxLayout()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            # ['Домен/Имя компьютера', 'MAC-адрес', 'Номер розетки',
            #  'Как подключен', 'Серверные приложения',
            #  'Windows OS', 'Windows OS key', 'Microsoft Office',
            #  'Microsoft Office key', 'Антивирус', 'Клиент электронной почты',
            #  'Прочее', 'Агент KES', 'Консультант', 'Гарант', '1C', 'КДС']
            ['Domain / Computer name', 'MAC address', 'Outlet number',
             'Como conectado', 'Aplicativos de servidor',
             'Sistema operacional Windows', 'Windows OS key', 'Microsoft Office',
             'Chave do Microsoft Office', 'Anti-Virus', 'Cliente de email',
             'Outro', 'Agente KES', 'Consultor', 'Fiador', '1C', 'KDS']
        )
        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setTextElideMode(Qt.ElideNone)
        self.table.setAlternatingRowColors(True)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

        table_buttons_layout = QHBoxLayout()
        add_table_row_button = QPushButton('Adicione um computador')
        add_table_row_button.setFixedSize(add_table_row_button.sizeHint())
        add_table_row_button.clicked.connect(self.add_table_row)
        delete_table_row_button = QPushButton('Soltar o computador')
        delete_table_row_button.setFixedSize(delete_table_row_button.sizeHint())
        delete_table_row_button.clicked.connect(self.delete_table_row)
        table_buttons_layout.addWidget(delete_table_row_button)
        table_buttons_layout.addWidget(add_table_row_button)
        table_buttons_layout.addStretch()

        table_layout.addWidget(self.table)
        table_layout.addLayout(table_buttons_layout)
        form_layout.addRow(table_layout)

        form_layout.addRow(buttons_layout)

    @pyqtSlot()
    def add_phone(self):
        phone_edit = QLineEdit()
        self.phone_edit.append(phone_edit)

        phone_layout = QHBoxLayout()
        phone_layout.addWidget(phone_edit)
        if len(self.phone_edit) < 3:
            phone_layout.addWidget(self.add_phone_button)
            self.layout().insertRow(5, "Número de telefone adicional:", phone_layout)
        else:
            self.add_phone_button.deleteLater()
            self.layout().insertRow(6, "Número de telefone adicional:", phone_layout)

    @pyqtSlot()
    def add_email(self):
        email_edit = QLineEdit()
        self.email_edit.append(email_edit)

        email_layout = QHBoxLayout()
        email_layout.addWidget(email_edit)
        if len(self.email_edit) < 3:
            email_layout.addWidget(self.add_email_button)
            self.layout().insertRow(
                5 + len(self.phone_edit), "E-mail adicional:", email_layout
            )
        else:
            self.add_email_button.deleteLater()
            self.layout().insertRow(
                6 + len(self.phone_edit), "E-mail adicional:", email_layout
            )

    @pyqtSlot(str)
    def changed_item_in_address_combobox(self, index):
        self.block_edit.clear()
        items = self.session.query(data.Block.name). \
            join(data.Address). \
            filter(data.Address.name == index). \
            values()
        self.block_edit.addItems(items)

    @pyqtSlot()
    def add_table_row(self):
        add_pcs = PCAdd(self.session, self.added_pcs)
        if add_pcs.exec_() == QDialog.Accepted:
            for pc in add_pcs.added_pcs:
                self.added_pcs.append(pc)
                self.model.appendRow([
                    QStandardItem(
                        QIcon(r'pics\pc.png'),
                        pc.pcname.domain.name + '/' + pc.pcname.name
                    ),
                    QStandardItem(pc.mac_address),
                    QStandardItem(pc.powersocket.name),
                    QStandardItem(pc.connectiontype.name),
                    QStandardItem(pc.app_server),
                    QStandardItem(pc.windows.name),
                    QStandardItem(pc.windows_os_key),
                    QStandardItem(pc.office.name),
                    QStandardItem(pc.ms_office_key),
                    QStandardItem(pc.antivirus.name),
                    QStandardItem(pc.mail_client),
                    QStandardItem(pc.comments),
                    QStandardItem('Existem' if pc.kes else 'Não'),
                    QStandardItem('Existem' if pc.consultant else 'Não'),
                    QStandardItem('Existem' if pc.guarantee else 'Não'),
                    QStandardItem('Existem' if pc.odin_s else 'Não'),
                    QStandardItem('Existem' if pc.kdc else 'Não')
                ])

    @pyqtSlot()
    def delete_table_row(self):
        index = self.table.selectionModel().selectedRows()
        try:
            element = self.model.takeRow(index[0].row())
        except IndexError:
            QMessageBox.warning(
                self, 'Erro',
                'Selecione a linha na tabela'
            )
            return
        self.added_pcs.remove(
            self.session.query(data.Pc). \
                filter_by(mac_address=element[1].text()).one()
        )

    @pyqtSlot()
    def validate_input(self):
        if not self.surname_edit.text() \
                or not self.name_edit.text() \
                or not self.room_edit.text() \
                or not self.login_edit.text():
            QMessageBox.warning(
                self, 'Atenção',
                "Campos: 'Sobrenome', 'Nome', 'Login', 'Sala'" +
                " -- obrigatórios"
            )
            return

        if not self.address_edit.currentText() \
                or not self.block_edit.currentText():
            QMessageBox.warning(
                self, 'Atenção',
                "Você deve adicionar pelo menos um endereço previamente"
            )
            return

        self.phone_numbers = [
            lineEdit.text() for lineEdit
            in self.phone_edit
            if lineEdit.text() != '+55()--'
        ]

        test_set = set()
        for phone_number in self.phone_numbers:
            if phone_number in test_set:
                QMessageBox.warning(
                    self, 'Atenção', 'Telefones são os mesmos'
                )
                return
            else:
                test_set.add(phone_number)

        for phone in self.phone_numbers:
            stmt = self.session.query(data.Phone). \
                filter(data.Phone.number == phone)

            if self.session.query(stmt.exists()).scalar():
                QMessageBox.warning(
                    self, 'Aviso', 'O telefone digitado já está no banco de dados'
                )
                return

        self.emails = [
            lineEdit.text() for lineEdit
            in self.email_edit
            if lineEdit.text()
        ]

        test_set = set()
        for email in self.emails:
            if email in test_set:
                QMessageBox.warning(
                    self, 'Aviso', 'correspondência de e-mail'
                )
                return
            else:
                test_set.add(email)

        for email in self.emails:
            stmt = self.session.query(data.Email). \
                filter(data.Email.email == email)

            if self.session.query(stmt.exists()).scalar():
                QMessageBox.warning(
                    self, 'Aviso', 'O e-mail inserido já existe no banco de dados'
                )
                return

        stmt = self.session.query(data.Employee). \
            filter(data.Employee.unique_login == self.login_edit.text())
        if self.session.query(stmt.exists()).scalar():
            QMessageBox.warning(
                self, 'Aviso', 'O login inserido já existe no banco de dados'
            )
            return

        self.process_data()
        if not self.accept():
            self.session.rollback()

    def process_data(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        employee = data.Employee(
            surname=self.surname_edit.text(),
            name=self.name_edit.text(),
            patronymic=self.patronymic_edit.text(),
            unique_login=self.login_edit.text(),
            comments=self.comments_edit.text(),
            shared_folder=self.shared_folder_edit.isChecked(),
            network_printer=self.network_printer_edit.isChecked()
        )

        employee.position = (
            get_or_create(
                self.session, data.Position,
                name=self.position_edit.currentText()
            )
        )

        employee.department = (
            get_or_create(
                self.session, data.Department,
                name=self.department_edit.currentText()
            )
        )

        for phone in self.phone_numbers:
            employee.phone.append(data.Phone(number=phone))

        for email in self.emails:
            employee.email.append(data.Email(email=email))

        block = self.session.query(data.Block). \
            join(data.Address). \
            filter(data.Block.name == self.block_edit.currentText()). \
            filter(data.Address.name == self.address_edit.currentText()). \
            one()

        room = self.session.query(data.Room). \
            join(data.Block). \
            filter(data.Room.name == self.room_edit.text()). \
            first()

        if not room:
            room = data.Room(name=self.room_edit.text())
            room.block = block

        employee.room = room
        employee.pc = self.added_pcs
        QApplication.restoreOverrideCursor()
