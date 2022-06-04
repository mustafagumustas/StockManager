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
        # reading saves of customer orders
        # converting customer order_id into string, we want 0001 not 1
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})
        self.load_order()
        # in order to create only one connect line
        # we need to iterate button names
        buttons = {
            self.b_filtercoffee,
            self.b_espresso,
            self.b_americano,
            self.b_latte,
        }
        for button in buttons:
            button.clicked.connect(self.order_click)

    def order_click(self):
        ordered = self.sender()
        self.df["orders"][self.df["#"] == self.order_id.text()] += [
            f",{ordered.text()}"
        ]
        self.load_order()

    def load_order(self):
        row = 0
        # getting orders from df
        current_order = (
            self.df["orders"][self.df["#"] == self.order_id.text()]
            .to_list()[0]
            .split(",")
        )
        self.tableWidget.setRowCount(len(current_order))
        #  populating tablewidget
        for i in range(len(current_order)):
            for order in current_order:
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(order)))
                row += 1


app = QApplication(sys.argv)
Main_Page = Main_Page()
Main_Page.show()
sys.exit(app.exec_())
