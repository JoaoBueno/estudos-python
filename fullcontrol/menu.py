import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp

menu_l0 = []
menu_l1 = []
menu_l2 = []
menu_l3 = []
menu_l4 = []
action = []


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create Menu Bar
        bar = self.menuBar()

        csvfile = open('1linha.csv', 'r')

        fieldnames = ('nivel', 'funcao', 'int', 'sep', 'opcao', 'prog')
        reader = csv.DictReader(csvfile, fieldnames, delimiter=';')
        i = 0
        for row in reader:
            # input(row['opcao'])
            if row['int'] == ' ':
                if row['nivel'] == '0':
                    if row['sep'] == '[':
                        menu_l0[-1].addSeparator()
                    menu_l0.append(bar.addMenu(row['opcao'].strip()))
                elif row['nivel'] == '1':
                    if row['sep'] == '[':
                        menu_l1[-1].addSeparator()
                    menu_l1.append(menu_l0[-1].addMenu(row['opcao'].strip()))
                elif row['nivel'] == '2':
                    if row['sep'] == '[':
                        menu_l2[-1].addSeparator()
                    menu_l2.append(menu_l1[-1].addMenu(row['opcao'].strip()))
                elif row['nivel'] == '3':
                    if row['sep'] == '[':
                        menu_l3[-1].addSeparator()
                    menu_l3.append(menu_l2[-1].addMenu(row['opcao'].strip()))
                elif row['nivel'] == '4':
                    if row['sep'] == '[':
                        menu_l4[-1].addSeparator()
                    menu_l4.append(menu_l3[-1].addMenu(row['opcao'].strip()))
            else:
                if row['nivel'] == '1':
                    if row['sep'] == '[':
                        menu_l0[-1].addSeparator()
                    action.append(QAction(row['opcao'].strip(), self))
                    menu_l0[-1].addAction(action[-1])
                    menu_l0[-1].triggered.connect(self.selected)
                    for l in action:
                        print('l ==> ' + l.text())
                elif row['nivel'] == '2':
                    if row['sep'] == '[':
                        menu_l1[-1].addSeparator()
                    action.append(QAction(row['opcao'].strip(), self))
                    menu_l1[-1].addAction(action[-1])
                    menu_l1[-1].triggered.connect(self.selected)
                    for l in action:
                        print('l ==> ' + l.text())
                elif row['nivel'] == '3':
                    if row['sep'] == '[':
                        menu_l2[-1].addSeparator()
                    action.append(QAction(row['opcao'].strip(), self))
                    menu_l2[-1].addAction(action[-1])
                    menu_l2[-1].triggered.connect(self.selected)
                    for l in action:
                        print('l ==> ' + l.text())
                elif row['nivel'] == '4':
                    if row['sep'] == '[':
                        menu_l3[-1].addSeparator()
                    action.append(QAction(row['opcao'].strip(), self))
                    menu_l3[-1].addAction(action[-1])
                    menu_l3[-1].triggered.connect(self.selected)
                    for l in action:
                        print('l ==> ' + l.text())
                elif row['nivel'] == '5':
                    if row['sep'] == '[':
                        menu_l4[-1].addSeparator()
                    action.append(QAction(row['opcao'].strip(), self))
                    menu_l4[-1].addAction(action[-1])
                    menu_l4[-1].triggered.connect(self.selected)
                    for l in action:
                        print('l ==> ' + l.text())
                # if action[-1].text() == '&DIPJ IPI (Ficha 32,33,34 e 35)':
                #     print(action[-1].text())
                #     i = i + 1
                #     print(i)

        # Create Root Menus
        file = bar.addMenu('File')
        edit = bar.addMenu('Edit')

        # Create Actions for menus
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')

        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')

        quit_action = QAction('&Quit', self)
        quit_action.setShortcut('Ctrl+Q')

        find_action = QAction('Find...', self)

        replace_action = QAction('Replace...', self)

        # Add actions to Menus
        file.addAction(new_action)
        file.addAction(save_action)
        file.addAction(quit_action)
        find_menu = edit.addMenu('Find')
        find_menu.addAction(find_action)
        find_menu.addAction(replace_action)

        # Events
        quit_action.triggered.connect(self.quit_trigger)
        file.triggered.connect(self.selected)

        self.setWindowTitle("My Menus")
        self.resize(600, 400)

        self.show()

    def quit_trigger(self):
        qApp.quit()

    def selected(self, q):
        print(q.text() + ' selected')


app = QApplication(sys.argv)
menus = Menu()
sys.exit(app.exec_())
