import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QIcon, QColor, QFont
import pandas as pd
import datetime
from PyQt5.QtCore import pyqtSlot


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
            self.win.showMaximized()
            self.close()
        else:
            print(self.username.text())
            print(self.password.text())
            pop_up_gen("Kullanici adi veya sifre hatali, tekrar deneyin!")


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
                {
                    "date": [str(date)],
                    "#": ["0001"],
                    "orders": "",
                    "cost": [0],
                }
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
        MainPage.openOrderPage()

    def openStockPage(self):
        self.win = Stock_Editor()
        self.win.showMaximized()
        self.close()

    def openOrderPage(self):
        self.win = OrderPage()
        self.win.showMaximized()
        self.close()

    def save_csv(self):
        # saving orders into csv with given orders and total cost info
        df.to_csv("june.csv", sep=";", index=False)


class Stock_Editor(QDialog):
    def __init__(self):
        super().__init__()
        # self.w = None

        # loading UI
        loadUi("stok.ui", self)

        # setting width of columns
        self.tableWidget.setColumnWidth(0, 450)
        self.tableWidget.setColumnWidth(1, 75)
        self.tableWidget.setColumnWidth(2, 40)
        self.tableWidget.setColumnWidth(3, 70)

        # reading csv file of stocks, if not found create and save empty one
        global col_names
        col_names = ["Kategori", "Ürün", "Fiyat", "Miktar", "Birim"]
        try:
            self.stocks = pd.read_csv("stok.csv", sep=";")
        except:
            self.stocks = pd.DataFrame(columns=col_names)

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

    def category(self):
        self.category_name.setEnabled(True)
        self.category_name.selectAll()
        self.category_name.del_()
        self.category_name.setFocus(True)
        self.category_name.setStyleSheet("border: 1px solid red;")

    def stok_onayla(self):
        empty = [
            col_name
            for i, col_name in enumerate(col_names[1:])
            if type(self.tableWidget.item(self.rowPosition, i)) == type(None)
        ]
        if len(empty) > 1:
            pop_up_gen(
                f"Bos urun eklenemez, bos satiri olan tabloyu onaylamaya calisiyorsunuz.",
                title="Urun tablosu hatasi!",
            )
        else:
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
        # user should't add new row without filling first rows cells
        global row_names
        empty = [
            col_name
            for i, col_name in enumerate(col_names[1:])
            if type(self.tableWidget.item(self.rowPosition, i)) == type(None)
        ]
        if len(empty) > 2:
            pop_up_gen(
                f"Bos urun eklenemez, {self.rowPosition+1} satirindaki degerleri eksiksiz giriniz",
                title="Urun tablosu hatasi!",
            )
        else:
            self.add_product.setEnabled(True)
            self.rowPosition += 1
            self.tableWidget.insertRow(self.rowPosition)
            self.combo = self.comboCompanies(self)
            self.tableWidget.setCellWidget(self.rowPosition, 3, self.combo)

    class comboCompanies(QComboBox):
        def __init__(self, parent):
            super().__init__(parent)
            self.addItems(["", "adet", "gram", "kilogram", "litre"])


class OrderPage(QDialog):
    def __init__(self):
        super().__init__()
        self.w = None
        loadUi("order.ui", self)
        self.order_id.setText(df["#"].iloc[[-1]].values[0])
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 45)

        self.delete_b_counter = 0

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

        self.b_filtercoffee.clicked.connect(self.button_loader)

        self.ok_button.clicked.connect(self.ok_)
        self.delete_button.clicked.connect(self.delete_button_clicked)
        self.cancel_button.clicked.connect(self.cancel_order)

        self.new_button_pos_x = 4
        self.new_button_pos_y = 0
        self.llllll = ["a", "b", "c"]

    @pyqtSlot()
    def button_loader(self):
        # this function creates
        Hlayout = QHBoxLayout(self)
        button2 = QPushButton(self.llllll[0], self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(button2.sizePolicy().hasHeightForWidth())
        button2.setSizePolicy(sizePolicy)
        button2.setMinimumSize(QSize(171, 61))
        font = QFont()
        font.setPointSize(16)
        button2.setFont(font)
        button2.setStyleSheet(
            """border-radius:16px;
            border-color: rgb(199, 98, 50);
            background-color:rgb(160, 140, 110);
            color:rgb(0, 0, 0)"""
        )
        button2.clicked.connect(lambda: print(button2.text()))
        spaceItem = QSpacerItem(10, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # Hlayout.addSpacerItem(spaceItem)
        Hlayout.addWidget(button2)
        # Hlayout.addSpacerItem(spaceItem)
        if self.new_button_pos_y % 2 == 1:
            self.urunbutonlari_layout.addLayout(Hlayout, self.new_button_pos_x, 1, 1, 1)
            self.new_button_pos_x += 1
        else:
            self.urunbutonlari_layout.addLayout(Hlayout, self.new_button_pos_x, 0, 1, 1)
        self.new_button_pos_y += 1

    def ok_(self):
        global new_order
        df["cost"].mask(
            ((df["#"] == 2) & (df["date"] == date)),
            MainPage.total,
            inplace=True,
        )

        last_order = str(df["orders"].iloc[[-1]].values[0]).split(",")
        last_order = [i for i in last_order if i != ""]
        df.loc[
            ((df["date"] == date) & (df["#"] == new_customer_id)),
            "orders",
        ] = ",".join(last_order)
        df.loc[
            ((df["date"] == date) & (df["#"] == new_customer_id)),
            "cost",
        ] = str(MainPage.total)
        df.to_csv("june.csv", sep=";", index=False)
        self.tableWidget.setRowCount(0)
        MainPage.new_order()
        self.close()

    def cancel_order(self):
        global df
        df = df[:-1]
        self.tableWidget.setRowCount(0)
        MainPage.new_order()
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
            ((df["date"] == date) & (df["#"] == new_customer_id)),
            "orders",
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
        # in order to delete rows, user must select one
        self.delete_b_counter += 1
        if self.tableWidget.selectedIndexes() and self.tableWidget.rowCount() > 0:
            row = self.tableWidget.currentIndex().row()
            orders = list(df["orders"].iloc[[-1]])[0].split(",")
            orders = [i for i in orders if i != ""]
            del orders[row]
            df.loc[
                ((df["date"] == date) & (df["#"] == new_customer_id)),
                "orders",
            ] = ",".join(orders)
            self.delete_b_counter = 0
        else:
            row = self.tableWidget.rowCount() - 1

        if self.delete_b_counter > 1:
            pop_up_gen("Urun silmek icin lutfen secim yapiniz")
            self.delete_b_counter = 1

        self.load_order()


class Order_Enter(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("order_enter.ui", self)
        self.setFixedSize(self.size())

        # removing second default tab
        self.tabWidget.removeTab(1)

        # setting columns
        self.columns = ["Ürün", "Fiyat"]
        self.tableWidget.setHorizontalHeaderLabels(self.columns)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 79)

        # adding rows
        self.rowPosition = self.tableWidget.rowCount()
        # there is a limit for buttons, for now its 4+1 as a test
        self.tableWidget.setRowCount(4)
        self.tableWidget.insertRow(self.rowPosition)
        self.onay_button.clicked.connect(self.print_list)

        # save point
        self.df_order = pd.DataFrame(columns=self.columns)

    def print_list(self):
        self.df_order["Ürün"] = [
            self.tableWidget.item(i, 0).text()
            for i in range(self.tableWidget.rowCount())
        ]
        self.df_order["Fiyat"] = [
            self.tableWidget.item(i, 1).text()
            for i in range(self.tableWidget.rowCount())
        ]
        print(self.df_order)


def pop_up_gen(message, title="Uyari"):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Question)
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.jpg"))
    MainPage = Order_Enter()
    MainPage.showMaximized()
    sys.exit(app.exec_())
