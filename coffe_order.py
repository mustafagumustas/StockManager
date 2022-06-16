import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QColor
import pandas as pd
import datetime

# nan degerleri oldugu icin hata veriyor
# csv ye hemen date ve # eklenmemeli
# bunun icin bir yol bul!


class Stock_Editor(QDialog):
    def __init__(self):
        super().__init__()
        self.w = None
        # loading UI
        loadUi("stok.ui", self)
        # setting width of columns
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 45)
        self.tableWidget.setColumnWidth(2, 45)
        self.tableWidget.setColumnWidth(3, 80)

        # reading csv file of stocks
        try:
            stocks = pd.read_csv("stok.csv", sep=";")
        except:
            pass

        self.rowPosition = self.tableWidget.rowCount()
        self.add_product.clicked.connect(self.add_row)
        self.onayla_button.clicked.connect(self.stok_onayla)
        self.category_name.setDisabled(True)
        self.add_category_b.clicked.connect(self.category)
        self.category_name_ok.clicked.connect(self.add_category)

        self.tabWidget.removeTab(1)
        self.tab_count = self.tabWidget.count()

    def add_category(self):
        tab_index = self.tabWidget.currentIndex()
        text = self.category_name.text()

        if self.tab_count == 1 and text != "Kategori adi" and text != "":
            self.tabWidget.setTabText(tab_index, str(text))
            self.tab_count += 1
        elif self.tab_count > 1 and text != "Kategori adi" and text != "":
            tab = QWidget()
            self.tabWidget.addTab(tab, str(text))
        self.category_name.setDisabled(True)
        self.category_name.setText("Kategori adi")
        self.tabWidget.tabBar().setTabTextColor(tab_index, QColor("black"))
        self.category_name.setStyleSheet("border: 1px solid black;")

    def category(self):
        self.category_name.setEnabled(True)
        self.category_name.selectAll()
        self.category_name.del_()
        self.category_name.setFocus(True)
        self.category_name.setStyleSheet("border: 1px solid red;")

    def stok_onayla(self):
        stocks = pd.DataFrame(columns=["Ürün", "Fiyat", "Miktar", "Birim"])
        stocks["Ürün"] = [
            self.tableWidget.item(row, 0).text()
            for row in range(self.tableWidget.rowCount())
        ]
        stocks["Fiyat"] = [
            self.tableWidget.item(row, 1).text()
            for row in range(self.tableWidget.rowCount())
        ]
        stocks["Miktar"] = [
            self.tableWidget.item(row, 2).text()
            for row in range(self.tableWidget.rowCount())
        ]
        stocks["Birim"] = [
            self.tableWidget.cellWidget(row, 3).currentText()
            for row in range(self.tableWidget.rowCount())
        ]
        stocks.to_csv("stocks.csv", sep=";", index=False)

    def add_row(self):
        self.tableWidget.insertRow(self.rowPosition)
        self.combo = self.comboCompanies(self)
        self.tableWidget.setCellWidget(self.rowPosition, 3, self.combo)

    class comboCompanies(QComboBox):
        def __init__(self, parent):
            super().__init__(parent)
            # self.setStyleSheet("font-size: 8px")
            self.addItems(["adet", "gram", "kilogram", "litre"])


class OrderPage(QDialog):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.w = None
        loadUi("order.ui", self)
        self.order_id.setText(MainPage.df["#"].iloc[[-1]].values[0])
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 45)

        self.cost_df = pd.read_csv(
            "beverage_cost.csv", sep=";", converters={"cost": lambda x: str(x)}
        )
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

        self.ok_button.clicked.connect(self.ok_)
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.cancel_button.clicked.connect(self.CloseEvent)

    def ok_(self):
        MainPage.df["cost"].mask(
            ((MainPage.df["#"] == 2) & (MainPage.df["date"] == MainPage.date)),
            MainPage.total,
            inplace=True,
        )

        last_order = str(MainPage.df["orders"].iloc[[-1]].values[0]).split(",")
        last_order = [i for i in last_order if i != ""]
        MainPage.df.loc[
            (
                (MainPage.df["date"] == MainPage.date)
                & (MainPage.df["#"] == MainPage.new_customer_id)
            ),
            "orders",
        ] = ",".join(last_order)
        MainPage.df.loc[
            (
                (MainPage.df["date"] == MainPage.date)
                & (MainPage.df["#"] == MainPage.new_customer_id)
            ),
            "cost",
        ] = str(MainPage.total)
        MainPage.df.to_csv("june.csv", sep=";", index=False)
        self.close()

    def CloseEvent(self):
        self.close()

    def order_click(self):
        # get the name of button triggered this function
        ordered = self.sender()
        last_order = list(
            MainPage.df["orders"]
            .loc[
                (
                    (MainPage.df["date"] == MainPage.date)
                    & (MainPage.df["#"] == MainPage.new_customer_id)
                )
            ]
            .values
        )
        last_order.append(f"{ordered.text()}")
        MainPage.df.loc[
            (
                (MainPage.df["date"] == MainPage.date)
                & (MainPage.df["#"] == MainPage.new_customer_id)
            ),
            "orders",
        ] = ",".join(last_order)
        self.load_order()

    def load_order(self):
        # getting orders from df
        current_order = (
            MainPage.df["orders"][
                (MainPage.df["#"] == self.order_id.text())
                & (MainPage.df["date"] == MainPage.date)
            ]
            .to_list()[0]
            .split(",")
        )
        current_order = [i for i in current_order if i != ""]
        self.tableWidget.setRowCount(len(current_order))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["orders", "cost"])
        #  populating tablewidget
        self.row = 0
        ttll = 0
        for order in current_order:
            self.tableWidget.setItem(self.row, 0, QTableWidgetItem(str(order)))
            new_cost = self.cost_df["cost"][self.cost_df["products"] == order].values[0]
            ttll += int(new_cost)
            MainPage.total = ttll

            self.tableWidget.setItem(self.row, 1, QTableWidgetItem(str(new_cost)))
            self.check.setText(str(MainPage.total))
            self.row += 1

    def delete_button_clicked(self):
        if self.tableWidget.selectedIndexes():
            row = self.tableWidget.currentIndex().row()
        else:
            row = self.tableWidget.rowCount() - 1
        if row >= 0:
            self.tableWidget.removeRow(row)
        orders = list(MainPage.df["orders"].iloc[[-1]])[0].split(",")
        orders = [i for i in orders if i != ""]
        del orders[row]
        MainPage.df.loc[
            (
                (MainPage.df["date"] == MainPage.date)
                & (MainPage.df["#"] == MainPage.new_customer_id)
            ),
            "orders",
        ] = ",".join(orders)
        self.load_order()


class MainPage(QDialog):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})
        loadUi("MainPage.ui", self)
        self.setWindowTitle("StockManager")
        self.siparisgir.clicked.connect(self.new_order)
        self.stokgir.clicked.connect(self.openStockPage)

    def new_order(self):
        # reading saves of customer orders
        # converting customer order_id into string, we want 0001 not 1
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})
        # todays date
        self.date = datetime.datetime.today().strftime("%d-%m-%Y")
        self.total = 0
        # creating customer id in 0000 format then changing label to it
        self.new_customer_id = ""
        if (self.date in self.df["date"].values) is False:
            new_df = pd.DataFrame(
                {"date": [str(self.date)], "#": ["0001"], "orders": "", "cost": [0],}
            )
            self.df = pd.concat([self.df, new_df], ignore_index=True, axis=0)
            self.new_customer_id = str("0001").zfill(4)
        else:
            self.new_customer_id = str(int(self.df["#"].iloc[[-1]]) + 1).zfill(4)
            new_df = pd.DataFrame(
                {
                    "date": [str(self.date)],
                    "#": [str(self.new_customer_id)],
                    "orders": "",
                    "cost": [0],
                }
            )
            self.df = pd.concat([self.df, new_df], ignore_index=True, axis=0)
        self.openOrderPage()

    def openStockPage(self):
        self.win = Stock_Editor()
        self.win.show()

    def openOrderPage(self):
        self.win = OrderPage()
        self.win.show()

    def save_csv(self):
        # saving orders into csv with given orders and total cost info
        self.df.to_csv("june.csv", sep=";", index=False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.jpg"))
    MainPage = MainPage()
    MainPage.show()
    sys.exit(app.exec_())
