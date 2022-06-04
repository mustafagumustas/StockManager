import sys
import PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pandas as pd
import os


class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        df = pd.read_csv("june.csv")

    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount)

    def _removeRow(self):
        if self.rowCount() > 0:
            self.removeRow(self.rowCount() - 1)


class Main_Page(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("order.ui", self)
        # self.orders_table = QTableWidget()
        self.loaddata()

    def loaddata(self):
        # reading saves of customer orders
        # converting customer order number into string, we want 0001 not 1
        df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})
        row = 0
        self.tableWidget.setRowCount(3)
        print(self.order_id.text(), df["#"][row])
        current_order = df["orders"][df["#"] == self.order_id.text()].to_list()
        print(current_order)
        for i in range(len(current_order)):
            for order in current_order[0].split(","):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(order)))
                row += 1


app = QApplication(sys.argv)
Main_Page = Main_Page()
Main_Page.show()
sys.exit(app.exec_())
