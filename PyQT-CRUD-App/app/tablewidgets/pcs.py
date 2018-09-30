#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Вкладка компьютеров
Guia Computador
"""
from app.editdialogs import pc
from app.db import data
from sqlalchemy import exc
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class PcsTable(QWidget):
    def __init__(self, session, parent):
        QDialog.__init__(self)
        self.session = session
        self.parent = parent
        self.build_layout()

    def build_layout(self):
        QVBoxLayout(self)

        self.model = QStandardItemModel()
        self.update_table_content()

        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.search_filter = QLineEdit()
        self.search_filter.setFixedWidth(500)
        self.search_filter.setClearButtonEnabled(True)
        self.search_filter.setPlaceholderText('Pesquisa de nome de domínio / nome do computador')
        self.search_filter.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setTextElideMode(Qt.ElideNone)
        self.table.setAlternatingRowColors(True)
        self.table.setModel(self.filter_proxy_model)
        self.table.resizeColumnsToContents()

        edit_button = QPushButton('Editar')
        edit_button.setFixedSize(edit_button.sizeHint())
        edit_button.clicked.connect(self.edit)
        self.layout().addWidget(self.search_filter)
        self.layout().addWidget(self.table)

    def update_table_content(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(
            # ['Домен/Имя компьютера', 'ФИО пользователя', 'MAC-адрес', 'Номер розетки',
            #  'Как подключен', 'Серверные приложения',
            #  'Windows OS', 'Windows OS key', 'Microsoft Office',
            #  'Microsoft Office key', 'Антивирус', 'Клиент электронной почты',
            #  'Прочее', 'Агент KES', 'Консультант', 'Гарант', '1C', 'КДС']
            ['Nome do domínio / computador', 'Nome do usuário', 'Endereço MAC', 'Número de soquetes',
             'Como conectado', 'Aplicativos de servidor',
             'Windows', 'Windows key', 'Microsoft Office',
             'Microsoft Office key', 'Anti-Virus', 'Cliente de e-mail',
             'Outro', 'Agente KES', 'Consultor', 'Fiador', '1C', 'KDS']
        )
        for pc in self.session.query(data.Pc):
            self.model.appendRow([
                QStandardItem(QIcon(r'pics\pc.png'), pc.pcname.domain.name + '/' + pc.pcname.name),
                QStandardItem(QIcon(r'pics\employee.png'), ';\n'.join([emp.fullname for emp in pc.employee])),
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
        try:
            self.table.resizeColumnsToContents()
        except Exception:
            pass

    @pyqtSlot()
    def edit(self):
        index = self.table.selectionModel().selectedRows()
        try:
            element = self.model.item(index[0].row())
        except IndexError:
            QMessageBox.warning(
                self, 'Erro',
                'Selecione a linha na tabela'
            )
            return
        pc_query_obj = self.session.query(data.Pc). \
            filter_by(mac_address=element[2].text()).one()
        try:
            edit_pc_window = pc.EditPc(self.session, pc_query_obj)
            if edit_pc_window.exec_() == QDialog.Accepted:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                self.session.commit()
                self.update_table_content()
                parent.employee_table.set_filter_comboboxes()
                parent.employee_table.self.fill_table()
                QApplication.restoreOverrideCursor()
                print("Zakommitili")
        except exc.IntegrityError as errmsg:
            print(errmsg)
            self.session.rollback()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Erro crítico no banco de dados")
            msg.setWindowTitle("Erro crítico")
            msg.setDetailedText(errmsg)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(sys.exit)
        else:
            print('Tudo com sucesso')