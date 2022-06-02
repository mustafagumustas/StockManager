import sys
import PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pandas as pd
import csv
import os

# SQL ile tarih barındıran bir colon olacak
# WHERE DATE ile o günün siparişleri getirilecek
# ancak yine  müşteri numarası olacak sadece birden fazla dosya açılmayacak
#   Date    |   Customer #  |               Orders                |   Cost    |
# 16.05.2022|      0002     | {"filter coffee": 2, "browinie": 1} |    20$    |
# just call above file and use Orders column and modify it with buttons


class Main_Page(QDialog):
    def __init__(self):
        super(Main_Page, self).__init__()
        loadUi("order.ui", self)
        # bu kısımda müşteri siparişlerinin kaydedileceği dosya init edilecek

        # order list
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnWidth(0, 135)
        self.tableWidget.setColumnWidth(1, 25)
        self.tableWidget.setColumnWidth(2, 110)
        self.b_filtercoffee.clicked.connect(self.order_filter)
        self.b_espresso.clicked.connect(self.order_esp)

    def order_filter(self):
        print("filter coffee")
        # self.tableWidget.setRowCount(50)
        tablerow = 0
        # self.tableWidget.insertRow(tablerow)
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(0)
        self.tableWidget.setItem(
            tablerow, 0, QTableWidgetItem(self.b_filtercoffee.text())
        )
        print(self.b_filtercoffee.text())

    def order_esp(self):
        print("espresso")

    def OpenFile(self):
        print("works")
        try:
            self.all_data = pd.read_csv(
                "/Volumes/GoogleDrive/My Drive/Python/side_projects/StockManager/june.csv"
            )
        except:
            print(
                "/Volumes/GoogleDrive/My Drive/Python/side_projects/StockManager/june.csv"
            )


app = QApplication(sys.argv)
Main_Page = Main_Page()
widget = QtWidgets.QStackedWidget()
widget.addWidget(Main_Page)
widget.setFixedHeight(650)
widget.setFixedWidth(850)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
