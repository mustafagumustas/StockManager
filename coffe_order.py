import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QColor
import pandas as pd
import datetime


class LoginPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("login.ui", self)
        self.admin_username = "must"
        self.admin_password = "1234"
        self.login_button.clicked.connect(self.log_user)

    def log_user(self):
        if (
            self.username.text() == self.admin_username
            and self.password.text() == self.admin_password
        ):
            self.win = MainPage()
            self.win.show()
            self.close()
        else:
            print(self.username.text())
            print(self.password.text())
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Kullanici adi veya sifre hatali, tekrar deneyin!")
            msg.setIcon(QMessageBox.Question)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()


class MainPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("MainPage.ui", self)
        global df, new_customer_id, total
        new_customer_id = ""
        total = 0
        df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})
        self.setWindowTitle("StockManager")
        self.siparisgir.clicked.connect(self.new_order)
        self.stokgir.clicked.connect(self.openStockPage)

    def new_order(self):
        global df, date, new_customer_id, total
        # reading saves of customer orders
        # converting customer order_id into string, we want 0001 not 1
        # todays date
        date = datetime.datetime.today().strftime("%d-%m-%Y")
        # creating customer id in 0000 format then changing label to it
        if (date in df["date"].values) is False:
            new_df = pd.DataFrame(
                {"date": [str(date)], "#": ["0001"], "orders": "", "cost": [0],}
            )
            df = pd.concat([df, new_df], ignore_index=True, axis=0)
            new_customer_id = str("0001").zfill(4)
        else:
            new_customer_id = str(int(df["#"].iloc[[-1]]) + 1).zfill(4)
            new_df = pd.DataFrame(
                {
                    "date": [str(date)],
                    "#": [str(new_customer_id)],
                    "orders": "",
                    "cost": [0],
                }
            )
            df = pd.concat([df, new_df], ignore_index=True, axis=0)
        MainPage.openOrderPage(self)

    def openStockPage(self):
        self.win = Stock_Editor()
        self.win.show()
        self.close()

    def openOrderPage(self):
        self.win = OrderPage()
        self.win.show()
        self.close()

    def save_csv(self):
        # saving orders into csv with given orders and total cost info
        df.to_csv("june.csv", sep=";", index=False)


class Stock_Editor(QDialog):
    def __init__(self):
        super().__init__()
        self.w = None

        # loading UI
        loadUi("stok.ui", self)

        # setting width of columns
        self.tableWidget.setColumnWidth(0, 450)
        self.tableWidget.setColumnWidth(1, 75)
        self.tableWidget.setColumnWidth(2, 40)
        self.tableWidget.setColumnWidth(3, 70)

        # reading csv file of stocks, if not found create and save empty one
        try:
            self.stocks = pd.read_csv("stok.csv", sep=";")
        except:
            self.stocks = pd.DataFrame(
                columns=["Kategori", "Ürün", "Fiyat", "Miktar", "Birim"]
            )

        # number of items in tablewidget
        self.rowPosition = self.tableWidget.rowCount()

        # push button connections
        # item to tablewidget
        self.add_product.clicked.connect(self.add_row)
        self.onayla_button.clicked.connect(self.stok_onayla)

        # category name
        self.category_name.setDisabled(True)
        self.add_category_b.clicked.connect(self.category)
        self.category_name_ok.clicked.connect(self.add_category)

        # there are 2 default tabs, removing one and making user edit first one
        self.tabWidget.removeTab(1)

        # nubmer of categories = tabs
        self.tab_count = self.tabWidget.count()
        if self.tab_count < 2:
            self.add_product.setEnabled(False)
            self.onayla_button.setEnabled(False)

        # disable add item button when nothing typed

    def add_category(self):
        tab_index = self.tabWidget.currentIndex()

        # user input of category name
        text = self.category_name.text()

        if self.tab_count == 1 and text != "Kategori adi" and text != "":
            self.tabWidget.setTabText(tab_index, str(text))
            # self.stocks[""]
            self.tab_count += 1
        elif self.tab_count > 1 and text != "Kategori adi" and text != "":
            tab = QWidget()
            self.tabWidget.addTab(tab, str(text))
        self.category_name.setDisabled(True)
        self.category_name.setText("Kategori adi")
        self.tabWidget.tabBar().setTabTextColor(tab_index, QColor("black"))
        self.category_name.setStyleSheet("border: 1px solid black;")
        self.add_product.setEnabled(True)
        self.onayla_button.setEnabled(True)
        if self.tableWidget.currentRow() == -1:
            self.tableWidget.insertRow(self.rowPosition)
            self.combo = self.comboCompanies(self)
            self.tableWidget.setCellWidget(self.rowPosition, 3, self.combo)
            # self.rowPosition += 1

    def category(self):
        self.category_name.setEnabled(True)
        self.category_name.selectAll()
        self.category_name.del_()
        self.category_name.setFocus(True)
        self.category_name.setStyleSheet("border: 1px solid red;")

    def stok_onayla(self):
        self.stocks["Kategori"] = [
            self.tabWidget.tabText(self.tabWidget.currentIndex())
            for row in range(self.tableWidget.rowCount())
        ]
        self.stocks["Ürün"] = [
            self.tableWidget.item(row, 0).text()
            for row in range(self.tableWidget.rowCount())
        ]
        self.stocks["Fiyat"] = [
            self.tableWidget.item(row, 1).text()
            for row in range(self.tableWidget.rowCount())
        ]
        self.stocks["Miktar"] = [
            self.tableWidget.item(row, 2).text()
            for row in range(self.tableWidget.rowCount())
        ]
        self.stocks["Birim"] = [
            self.tableWidget.cellWidget(row, 3).currentText()
            for row in range(self.tableWidget.rowCount())
        ]
        self.stocks.to_csv("stocks.csv", sep=";", index=False)
        self.add_product.setEnabled(True)

    def add_row(self):
        if self.tableWidget.item(self.rowPosition - 1, 0):
            if self.tableWidget.item(self.rowPosition - 1, 0).text():
                self.add_product.setEnabled(True)
                self.tableWidget.insertRow(self.rowPosition)
                self.combo = self.comboCompanies(self)
                self.tableWidget.setCellWidget(self.rowPosition, 3, self.combo)
            else:
                print("empty")
        else:
            self.add_product.setEnabled(False)
            msg = QMessageBox()
            msg.setWindowTitle("Urun tablosu hatasi!")
            msg.setText("Bos urun eklenemez, urun adi girerek tekrar deneyin!")
            msg.setIcon(QMessageBox.Question)
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        self.rowPosition += 1

    class comboCompanies(QComboBox):
        def __init__(self, parent):
            super().__init__(parent)
            # self.setStyleSheet("font-size: 8px")
            self.addItems(["", "adet", "gram", "kilogram", "litre"])


class OrderPage(QDialog):
    window_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.w = None
        loadUi("order.ui", self)
        self.order_id.setText(df["#"].iloc[[-1]].values[0])
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
        self.cancel_button.clicked.connect(self.cancel_order)

    def ok_(self):
        global new_order
        df["cost"].mask(
            ((df["#"] == 2) & (df["date"] == date)), MainPage.total, inplace=True,
        )

        last_order = str(df["orders"].iloc[[-1]].values[0]).split(",")
        last_order = [i for i in last_order if i != ""]
        df.loc[
            ((df["date"] == date) & (df["#"] == new_customer_id)), "orders",
        ] = ",".join(last_order)
        df.loc[((df["date"] == date) & (df["#"] == new_customer_id)), "cost",] = str(
            MainPage.total
        )
        df.to_csv("june.csv", sep=";", index=False)
        self.tableWidget.setRowCount(0)
        MainPage.new_order(self)
        self.close()

    def cancel_order(self):
        global df
        df = df[:-1]
        print(df)
        self.tableWidget.setRowCount(0)
        MainPage.new_order(self)
        self.close()

    def order_click(self):
        # get the name of button triggered this function
        ordered = self.sender()
        last_order = list(
            df["orders"]
            .loc[((df["date"] == date) & (df["#"] == new_customer_id))]
            .values
        )
        last_order.append(f"{ordered.text()}")
        df.loc[
            ((df["date"] == date) & (df["#"] == new_customer_id)), "orders",
        ] = ",".join(last_order)
        self.load_order()

    def load_order(self):
        # getting orders from df
        current_order = (
            df["orders"][(df["#"] == self.order_id.text()) & (df["date"] == date)]
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
        orders = list(df["orders"].iloc[[-1]])[0].split(",")
        orders = [i for i in orders if i != ""]
        del orders[row]
        df.loc[
            ((df["date"] == date) & (df["#"] == new_customer_id)), "orders",
        ] = ",".join(orders)
        self.load_order()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.jpg"))
    LoginPage = LoginPage()
    LoginPage.show()
    sys.exit(app.exec_())
