import sys
import PyQt5
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import pandas as pd
import csv
import os

# SQL ile tarih barındıran bir colon olacak
# WHERE DATE ile o günün siparişleri getirilecek
# ancak yine  müşteri numarası olacak sadece birden fazla dosya açılmayacak
#   Date    |   Customer #  |               Orders                |   Cost    |
# 16.05.2022|      0002     | {"filter coffee": 2, "browinie": 1} |    20$    |
# just call above file and use Orders column and modify it with buttons


class Main_Page(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        # QtCore.QAbstractTableModel.__init__(self, parent)

        loadUi("order.ui", self)
        # bu kısımda müşteri siparişlerinin kaydedileceği dosya init edilecek

        # order list
        data = pd.read_csv("june.csv")
        self.model = TableModel(data)
        self.tableView.setModel(self.model)


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


app = QtWidgets.QApplication(sys.argv)
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
