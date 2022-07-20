import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QSize, QSettings
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


class Preferences(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("preferences.ui", self)
        self.setWindowTitle("Preferences")
        self.kupon_indirimi_check.stateChanged.connect(self.kupon_indirimi_gorunurluk)

    def kupon_indirimi_gorunurluk(self):
        state = self.kupon_indirimi_check.isChecked()
        # kupon_indirimi_check
        if state == True:
            MainPage.kupon_label.setVisible(True)
        else:
            MainPage.kupon_label.setVisible(False)


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("mainn.ui", self)

        # menubar
        bar = self.menuBar()
        # add File section into menubar
        file = bar.addMenu("Dosya")

        # adding more items to file in menubar
        actionNew = QAction("Yeni", self)
        file.addAction(actionNew)
        actionOpen = QAction("Aç", self)
        file.addAction(actionOpen)
        actionPref = QAction("Pref", self)
        file.addAction(actionPref)

        edit = bar.addMenu("Düzenle")
        edit.addAction("Düzenle")

        actionNew.triggered.connect(lambda: print("hey"))
        actionOpen.triggered.connect(lambda: print("ey open up"))
        actionPref.triggered.connect(lambda: self.preff())
        #
        # some global variables acrorr the app
        self.date = datetime.datetime.today().strftime("%d-%m-%Y")
        self.total = 0
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})

        self.setWindowTitle("StockManager")
        self.new_order()
        self.ui = OrderPage()

        # button functions
        self.order_page_button.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_1)
        )

        # orderpage button functional connections
        #
        # in order to create only one connect line
        # we need to iterate button names
        buttons = {
            self.b_filtercoffee,
            self.b_espresso,
            self.b_americano,
            self.b_latte,
        }
        for button in buttons:
            button.clicked.connect(self.ui.order_click)

        self.ok_button.clicked.connect(self.ui.ok_)
        self.delete_button.clicked.connect(self.ui.delete_button_clicked)
        self.cancel_button.clicked.connect(self.ui.cancel_order)

        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 45)

    def preff(self):
        self.win = Preferences()
        self.win.show()

    def new_order(self):
        # converting customer order_id into string, we want 0001 not 1
        # todays date
        # creating customer id in 0000 format then changing label to it
        if (self.date in self.df["date"].values) is False:
            new_customer_id = str("0001").zfill(4)
            self.order_id.setText(new_customer_id)
            return new_customer_id
        else:
            new_customer_id = str(int(self.df["#"].iloc[[-1]]) + 1).zfill(4)
            self.order_id.setText(new_customer_id)
            return new_customer_id


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
        self.delete_b_counter = 0
        self.cost_df = pd.read_csv(
            "beverage_cost.csv", sep=";", converters={"cost": lambda x: str(x)}
        )
        self.current_customer = None
        self.current_orders = []
        # self.b_filtercoffee.clicked.connect(self.button_loader)

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
        Hlayout.addWidget(button2)
        if self.new_button_pos_y % 2 == 1:
            self.urunbutonlari_layout.addLayout(Hlayout, self.new_button_pos_x, 1, 1, 1)
            self.new_button_pos_x += 1
        else:
            self.urunbutonlari_layout.addLayout(Hlayout, self.new_button_pos_x, 0, 1, 1)
        self.new_button_pos_y += 1

    def ok_(self):
        # the customer finished the ordering and its time to save
        # information of current order
        data = [
            MainPage.date,
            self.current_customer.id,
            ",".join(self.current_customer.orders),
            self.current_customer.cost,
        ]

        new_df = pd.DataFrame([data], columns=MainPage.df.columns)
        # adding row to main data save
        MainPage.df = pd.concat([MainPage.df, new_df], ignore_index=True, axis=0)

        # clearing tablewidget for new customers
        self.current_orders = []
        MainPage.tableWidget.setRowCount(0)
        MainPage.new_order()
        MainPage.check.setText(str("0"))
        MainPage.df.to_csv("june.csv", sep=";", index=False)

    def cancel_order(self):
        # canceling all of the orders no saving clearing tablewidget
        MainPage.tableWidget.setRowCount(0)
        self.current_orders = []
        self.current_customer.orders = []
        self.current_customer.cost = 0
        MainPage.check.setText(str("0"))
        self.load_order()

    def order_click(self):
        # get the name of button triggered this function
        ordered = self.sender().text()
        self.current_orders.append(ordered)
        self.current_customer = customer(MainPage.new_order(), self.current_orders, 0)
        self.load_order()

    def load_order(self):
        # populating tablewidget
        current_order = self.current_customer.orders
        current_order = [i for i in current_order if i != ""]
        MainPage.tableWidget.setRowCount(len(current_order))
        MainPage.tableWidget.setColumnCount(2)
        MainPage.tableWidget.setHorizontalHeaderLabels(["orders", "cost"])
        self.row = 0
        self.current_customer.cost = 0
        for order in self.current_customer.orders:
            MainPage.tableWidget.setItem(self.row, 0, QTableWidgetItem(str(order)))
            # calculating current cost
            new_cost = self.cost_df["cost"][self.cost_df["products"] == order].values[0]
            self.current_customer.cost += int(new_cost)
            MainPage.total = self.current_customer.cost
            MainPage.tableWidget.setItem(self.row, 1, QTableWidgetItem(str(new_cost)))
            MainPage.check.setText(str(MainPage.total))
            self.row += 1

    def delete_button_clicked(self):
        # in order to delete rows, user must select one
        self.delete_b_counter += 1
        if (
            MainPage.tableWidget.selectedIndexes()
            and MainPage.tableWidget.rowCount() > 0
        ):
            row = MainPage.tableWidget.currentIndex().row()
            del self.current_customer.orders[row]
            self.delete_b_counter = 0
        else:
            row = MainPage.tableWidget.rowCount() - 1

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


class customer:
    # this class is for saving customers info
    # it contains the id of the customer for that day
    # products that customer ordered and total cost
    def __init__(self, id, orders, cost):
        self.id = id
        self.orders = orders
        self.cost = cost


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logo.jpg"))
    MainPage = MainPage()
    MainPage.showMaximized()
    sys.exit(app.exec_())
