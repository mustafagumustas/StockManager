import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sqlite3


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("table_view.ui", self)

        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 350)
        self.tableWidget.setHorizontalHeaderLabels(["City", "Country", "Subcountry"])
        self.loaddata()

    def loaddata(self):
        connection = sqlite3.connect("data.sqlite")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM worldcities LIMIT 50"

        self.tableWidget.setRowCount(50)
        tablerow = 0
        for row in cur.execute(sqlquery):
            self.tableWidget.setItem(tablerow, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QTableWidgetItem(row[1]))
            tablerow += 1


# main
app = QApplication(sys.argv)
mainwindow = MainWindow()

widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedHeight(700)
widget.setFixedWidth(1120)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
