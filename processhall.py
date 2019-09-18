#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import (QFrame, QDesktopWidget, QMainWindow, QAction, QWidget, qApp, QGridLayout,
    QPushButton, QApplication, QVBoxLayout,QHBoxLayout, QLabel, QLineEdit, QComboBox, QCalendarWidget)
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QRect, pyqtSlot
from PyQt5.QtGui import (QIcon, QFont, QPainter, QBrush, QColor, QKeyEvent)

import yaml

from scale.scale import Scale

GLOBAL_PRODUCTS = None
with open("products.yml", 'r') as ymlfile:
    GLOBAL_PRODUCTS = yaml.safe_load(ymlfile)

# customers.yml is excluded from the repo, example in customers_example.yml
GLOBAL_CUSTOMERS = None
with open("customers.yml", 'r') as ymlfile:
    GLOBAL_CUSTOMERS = yaml.safe_load(ymlfile)

class ScaleFrame(QFrame):
    def __init__(self, parent):
        super(ScaleFrame, self).__init__(parent)
        self.parent = parent
        print('ScaleFrame: my parent is',self.parent)
        self.initFrame()

    def initFrame(self):
        self.timer = QBasicTimer()
        self.myscale = Scale(10202)

        self.lbl_weight = QLabel(self)
        self.lbl_weight.setObjectName('lbl_weight')
        self.lbl_weight.setText("0.000")
        self.lbl_weight.resize(500, 100)
        self.lbl_weight.move(50, 50)

        lbl_unit = QLabel(self)
        lbl_unit.setObjectName('lbl_unit')
        lbl_unit.setText("kg")
        lbl_unit.resize(100, 120)
        lbl_unit.move(350, 40)

        #self.lbl_status = QLabel(self)
        #self.lbl_status.setText("MAYBE ON")
        #self.lbl_status.resize(100, 100)
        #self.lbl_status.move(700, 10)


        #qbtn = QPushButton('Jalla', self)
        #qbtn.clicked.connect(QApplication.instance().quit)
        #qbtn.resize(qbtn.sizeHint())
        #qbtn.move(150, 150)

        self.setObjectName('ScaleFrame')
        self.setStyleSheet("""
            #ScaleFrame {
                background-color: #cfcfcf;
            }
            .QLabel#lbl_weight {
                font-size:100pt;
                color: #ff0000;
            }
            .QLabel#lbl_unit {
                font-size:100pt;
                color: #000000;
            }
            .QLabel {
                font-size:22pt;
                color: #000000;
            }
        """)
        self.start_timer()

    def start_timer(self):
        self.timer.start(100, self)

    def timerEvent(self, event):
        '''handles timer event'''
        if event.timerId() == self.timer.timerId():
            time_last_received, weight = self.myscale.return_last_weight()
            self.window().statusbar.showMessage(F"Last received: {time_last_received}")
            self.lbl_weight.setText(F"{weight:.3f}")
        else:
            super(Board, self).timerEvent(event)


class LabelFrame(QWidget):
    #asignal = pyqtSignal(str)

    def __init__(self, parent):
        global GLOBAL_PRODUCTS

        super(LabelFrame, self).__init__(parent)
        self.parent = parent
        print('LabelFrame: my parent is',self.parent)
        self.initFrame()

    def initFrame(self):
        self.setFixedWidth(500)

        layout = QGridLayout()

        lbl_product = QLabel('Product')
        self.input_product = QComboBox(self)
        for product in GLOBAL_PRODUCTS:
            self.input_product.addItem(GLOBAL_PRODUCTS[product]['friendlyname']['NOR'])

        lbl_language = QLabel('Language')
        self.input_language = QComboBox(self)
        self.input_language.addItems(['Norwegian', 'English', 'Spanish', 'Dutch', 'French'])

        lbl_grade = QLabel('Grade')
        self.input_grade = QComboBox(self)
        self.input_grade.addItem('Select a product')

        lbl_processing = QLabel('Processing')
        self.input_processing = QComboBox(self)
        self.input_processing.addItem('Select a product')

        lbl_batch = QLabel('Batch')
        self.input_batch = QLineEdit(self)
        self.input_batch.setText('000001')

        lbl_harvest_date = QLabel('Harvest date')
        self.input_harvest_date = QCalendarWidget(self)
        self.input_harvest_date.resize(100,50)

        lbl_customer = QLabel('Customer')
        self.input_customer = QComboBox(self)
        self.input_customer.setEditable(True)
        self.input_customer.addItem('CUSTOMER - You can edit this field if you want')
        for customer in GLOBAL_CUSTOMERS:
            self.input_customer.addItem(GLOBAL_CUSTOMERS[customer]['printablename'])

        self.btn_print_label = QPushButton('Print Label', self)
        self.btn_print_label.setFixedHeight(50)


        layout.setSpacing(10)
        layout.addWidget(lbl_language, 1, 0)
        layout.addWidget(self.input_language, 1, 1)
        layout.addWidget(lbl_product, 2, 0)
        layout.addWidget(self.input_product, 2, 1)
        layout.addWidget(lbl_grade, 3, 0)
        layout.addWidget(self.input_grade, 3, 1)
        layout.addWidget(lbl_processing, 4, 0)
        layout.addWidget(self.input_processing, 4, 1)
        layout.addWidget(lbl_batch, 5, 0)
        layout.addWidget(self.input_batch, 5, 1)
        layout.addWidget(lbl_harvest_date, 6, 0)
        layout.addWidget(self.input_harvest_date, 6, 1)
        layout.addWidget(lbl_customer, 7, 0)
        layout.addWidget(self.input_customer, 7, 1)
        layout.addWidget(self.btn_print_label, 8, 1)
        self.setLayout(layout)

        # Set up signals
        self.input_product.currentIndexChanged[int].connect(self.on_product_combo_currentIndexChanged)
        self.input_language.activated[str].connect(self.on_language_combo_activated)
        self.btn_print_label.clicked.connect(self.on_print_label_clicked)


    @pyqtSlot()
    def on_print_label_clicked(self):
        print('PRINTING LABEL')

    @pyqtSlot(str)
    def on_language_combo_activated(self, text):
        print(text)
        #self.asignal.emit('selected', text)
    def on_product_combo_currentIndexChanged(self, index):
        self.input_grade.clear()
        print('index', index)
        #product = text
        for i, grade in enumerate(GLOBAL_PRODUCTS[index]['grades']): # A dictionary
            print(grade)
            self.input_grade.addItem(grade[i])

        self.input_processing.clear()
        print('index', index)
        #product = text
        for i, process in enumerate(GLOBAL_PRODUCTS[index]['processing']): # A dictionary
            print(process)
            self.input_processing.addItem(process)
        
        
        #print(self.productsfile)
        #print(text)



class CentralFrame(QFrame):
    def __init__(self, parent):
        super(CentralFrame, self).__init__(parent)
        self.parent = parent
        print('CentralFrame: my parent is',self.parent)
        self.initFrame()

    def initFrame(self):
        layout = QHBoxLayout()


        #printbtn = QPushButton('Print Label', self)
        #printbtn.clicked.connect(QApplication.instance().quit)
        #printbtn.resize(printbtn.sizeHint())

        self.labelframe = LabelFrame(self)
        self.scaleframe = ScaleFrame(self)


        layout.addWidget(self.labelframe)
        layout.addWidget(self.scaleframe)
        #layout.addWidget(printbtn)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        self.parent = parent
        print('MainWindow: my parent is',self.parent)
        self.initUI()

    def initUI(self):
        centralframe = CentralFrame(self)
        self.setCentralWidget(centralframe)

       #self.centralframe.labelframe.asignal.connect(self.widgetB.on_procStart)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setMenuRole(QAction.NoRole)
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'icon.png')
        self.setWindowIcon(QIcon(path))
        self.setGeometry(1000, 600, 1000, 600)
        self.center()
        self.setWindowTitle('Statsnail AS - Seafood Labelling Software')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

#https://www.riverbankcomputing.com/static/Docs/PyQt4/qevent.html
    def keyPressEvent(self, event: QKeyEvent) -> None:
        try:
            print(event.type())
            if event.key() in (Qt.Key_Plus):
                print('key plus pressed, ignore')
                ev.ignore()
                return True
        except:
            pass

    @pyqtSlot() # https://stackoverflow.com/questions/49480437/pyqt5-qcombobox-how-do-i-use-the-selected-value-of-the-user-to-execute-a-specif
    def on_click(self):
        print('Clicked self?')

    def onActivated(self, text):
        self.lbl_customer = text


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parent = QMainWindow()
    mainwindow = MainWindow(parent)
    sys.exit(app.exec_())