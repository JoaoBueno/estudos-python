#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Добавляем методы для подтверждения закрытия диалоговых окон
Adicione métodos para confirmar as caixas de diálogo de fechamento
"""
from PyQt5.QtWidgets import QDialog, QMessageBox

class Dialog(QDialog):

    def closeEvent(self, evnt):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Notificação')
        msg_box.setText('Os dados não serão salvos.')
        msg_box.setStandardButtons(
            QMessageBox.Yes | QMessageBox.Cancel
        )
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Sair')
        buttonN = msg_box.button(QMessageBox.Cancel)
        buttonN.setText('Cancelar')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            QDialog.closeEvent(self, evnt)
        elif msg_box.clickedButton() == buttonN:
            evnt.ignore()

    def accept(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Notificação')
        msg_box.setText('Confirme a entrada de dados')
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = msg_box.button(QMessageBox.Yes)
        buttonY.setText('Sim')
        buttonN = msg_box.button(QMessageBox.No)
        buttonN.setText('Não')
        msg_box.exec_()

        if msg_box.clickedButton() == buttonY:
            QDialog.accept(self)
            return True
        else:
            return False