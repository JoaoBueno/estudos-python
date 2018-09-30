#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Добавление компьютеров из списка
Adicionando computadores da lista
"""
from app.db import data
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *


class PCAdd(QDialog):
    def __init__(self, session, pcs_to_ignore):
        QDialog.__init__(self)
        self.session = session
        self.pcs_to_ignore = pcs_to_ignore
        self.added_pcs = []
        self.init_window()
        self.build_layout()

    def init_window(self):
        self.setFixedSize(800, 450)
        self.setWindowModality(2)
        self.setWindowTitle('Adicionando Computadores')
        self.setWindowIcon(QIcon(r'pics\pc.png'))

    def build_layout(self):
        QVBoxLayout(self)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(
            # ['Домен/Имя компьютера', 'MAC-адрес', 'Номер розетки',
            #  'Как подключен', 'Серверные приложения',
            #  'Windows OS', 'Windows OS key', 'Microsoft Office',
            #  'Microsoft Office key', 'Антивирус', 'Клиент электронной почты',
            #  'Прочее', 'Агент KES', 'Консультант', 'Гарант', '1C', 'КДС']
            ['Domain / Computer name', 'MAC address', 'Outlet number',
             'Como conectado', 'Aplicativos de servidor',
             'Windows', 'Windows key', 'Microsoft Office',
             'Microsoft Office key', 'Anti-Virus', 'Cliente de email',
             'Outro', 'Agente KES', 'Consultor', 'Fiador', '1C', 'KDS']
        )

        for pc in [pc for pc in self.session.query(data.Pc).all() if pc not in self.pcs_to_ignore]:
            self.model.appendRow([
                QStandardItem(QIcon(r'pics\pc.png'), pc.pcname.domain.name + '/' + pc.pcname.name),
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

        self.filter_proxy_model = QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.setFilterKeyColumn(0)

        self.search_filter = QLineEdit()
        self.search_filter.setFixedWidth(500)
        self.search_filter.setClearButtonEnabled(True)
        self.search_filter.setPlaceholderText('Pesquisa de nome de domínio / nome do computador')
        self.search_filter.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        tooltip = QLabel('<p>Dica: mantenha pressionada a tecla CTRL para selecionar várias entradas</p>')

        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setTextElideMode(Qt.ElideNone)
        self.table.setAlternatingRowColors(True)
        self.table.setModel(self.filter_proxy_model)
        self.table.resizeColumnsToContents()

        self.add_pcs = QPushButton('Adicionar selecionado')
        self.add_pcs.setFixedSize(self.add_pcs.sizeHint())
        self.add_pcs.clicked.connect(self.add_selected_pcs)

        self.layout().addWidget(self.search_filter)
        self.layout().addWidget(tooltip)
        self.layout().addWidget(self.table)
        self.layout().addWidget(self.add_pcs)

    @pyqtSlot()
    def add_selected_pcs(self):
        indexes = self.table.selectionModel().selectedRows()
        for index in indexes:
            mac = self.model.item(index.row(), 1).text()
            self.added_pcs.append(
                self.session.query(data.Pc). \
                    filter_by(mac_address=mac).one()
            )
        QDialog.accept(self)
