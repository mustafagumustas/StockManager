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

        # kupon indirimi
        self.kupon_indirimi_checkbox.setChecked(
            MainPage.settings.value("pref_kupon_kodu_goster")
        )
        self.kupon_indirimi_checkbox.stateChanged.connect(
            self.kupon_indirimi_gorunurluk
        )
        self.kategori_checkbox.setChecked(MainPage.settings.value("kategori_kullanimi"))

        # kategori
        self.kategori_checkbox.stateChanged.connect(self.kategori_durumu)

    def kategori_durumu(self):
        kategori_durumu = self.kategori_checkbox.isChecked()
        MainPage.settings.setValue("kategori_kullanimi", kategori_durumu)

    def kupon_indirimi_gorunurluk(self):
        state = self.kupon_indirimi_checkbox.isChecked()
        MainPage.kupon_label.setVisible(state)
        MainPage.settings.setValue("pref_kupon_kodu_goster", state)


class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("mainn.ui", self)
        ############################
        #         MENUBAR          #
        ############################
        bar = self.menuBar()
        # add File section into menubar
        file = bar.addMenu("Dosya")

        # adding more items to file in menubar
        actionNew = QAction("Yeni", self)
        actionOpen = QAction("Aç", self)
        actionPref = QAction("Tercihler", self)

        file.addAction(actionOpen)
        file.addAction(actionNew)
        file.addSeparator()
        file.addAction(actionPref)

        #
        # menubar duzenlemesi
        #
        siparis = bar.addMenu("Siparis")
        actionItems = QAction("Ürünler", self)
        actionAccItemFromFile = QAction("Dosya Üzerinden Urun Ekle", self)
        siparis.addAction(actionItems)
        siparis.addAction(actionAccItemFromFile)

        edit = bar.addMenu("Düzenle")
        edit.addAction("Düzenle")

        actionItems.triggered.connect(lambda: self.item_add())
        actionNew.triggered.connect(lambda: print("hey"))
        actionOpen.triggered.connect(lambda: print("ey open up"))
        actionPref.triggered.connect(lambda: self.preff())

        ############################
        #         SETTINGS         #
        ############################
        self.settings = QSettings("Mustafa Gumustas", "StockManager")
        self.cost_filename = self.settings.value("items_cost_file_name")
        # ORDER PAGE
        # self.settings.setValue("ilk_kullanici_order_yukeleme_sor", 0)

        self.settings.value("kategori_kullanimi")
        ############################
        #        Preferences       #
        ############################
        self.kupon_label.setVisible(self.settings.value("pref_kupon_kodu_goster"))

        #
        # some global variables across the app
        self.date = datetime.datetime.today().strftime("%d-%m-%Y")
        self.total = 0
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})

        self.setWindowTitle("StockManager")
        self.new_order()
        self.ui = OrderPage()

        # button functions
        if self.settings.value("continue_use_selected_csv") == 16384:
            self.button_loader()
        else:
            pass
        # self.b_filtercoffee.clicked.connect(self.button_loader)
        self.order_page_button.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_1)
        )
        self.stok_page_button.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_2)
        )

        self.ok_button.clicked.connect(self.ui.ok_)
        self.delete_button.clicked.connect(self.ui.delete_button_clicked)
        self.cancel_button.clicked.connect(self.ui.cancel_order)

        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 45)

    def item_add(self):
        self.win = Order_Enter()
        self.win.show()

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

    @pyqtSlot()
    def button_loader(self):
        self.new_button_pos_x = 0
        self.new_button_pos_y = 0
        itttmes = pd.read_csv(self.settings.value("items_cost_file_name"), ";")
        for i, item in enumerate(itttmes["Ürün"].values):
            if self.new_button_pos_y % 2 == 1:
                self.urunbutonlari_layout.addLayout(
                    self.button_creator(item), self.new_button_pos_x, 1, 1, 1
                )
                self.new_button_pos_x += 1
            else:
                self.urunbutonlari_layout.addLayout(
                    self.button_creator(item), self.new_button_pos_x, 0, 1, 1
                )
            self.new_button_pos_y += 1

    def button_creator(self, text):
        Hlayout = QHBoxLayout(self)
        button = QPushButton(text, self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy)
        button.setMinimumSize(QSize(171, 61))
        font = QFont()
        font.setPointSize(16)
        button.setFont(font)
        button.setStyleSheet(
            """border-radius:16px;
            border-color: rgb(199, 98, 50);
            background-color:rgb(160, 140, 110);
            color:rgb(0, 0, 0)"""
        )
        button.setObjectName(f"b_{text}")
        button.clicked.connect(self.ui.order_click)
        Hlayout.addWidget(button)
        return Hlayout


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
        try:
            self.cost_df = pd.read_csv(
                self.cost_filename, sep=";", converters={"Fiyat": lambda x: str(x)}
            )
        except:
            pass
        self.current_customer = None
        self.current_orders = []

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
        if self.current_customer is not None:
            self.current_orders = []
            self.current_customer.orders = []
            self.current_customer.cost = 0
            MainPage.check.setText(str("0"))
            self.load_order()
        else:
            pass

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
            new_cost = self.cost_df["Fiyat"][self.cost_df["Ürün"] == order].values[0]
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
        self.setWindowTitle("Ürün Tablosu")
        self.df_order = None
        self.setFixedSize(self.size())

        # removing second default tab
        self.tabWidget.removeTab(1)

        # loading items into table if user wanted to use the same file later
        if MainPage.settings.value("continue_use_selected_csv") == 16384:
            self.order_loader()
        else:
            pass

        # setting columns
        # if MainPage.settings.value("kategori_kullanimi"):
        #     pass
        # else:
        self.columns = ["Ürün", "Fiyat"]

        self.urun_tablosu.setHorizontalHeaderLabels(["Ürün", "Fiyat"])
        self.urun_tablosu.setColumnCount(2)
        self.urun_tablosu.setColumnWidth(0, 250)
        self.urun_tablosu.setColumnWidth(1, 79)
        # PREFERENCES
        if MainPage.settings.value("kategori_kullanimi"):
            pass
        else:
            self.tabWidget.setParent(None)
            # creating page from scratch without categories
            self.gridLayout = QGridLayout(self)
            self.gridLayout.setObjectName("gridLayout")
            self.horizontalLayout = QHBoxLayout()
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.urun_sayisi = QSpinBox(self)
            self.urun_sayisi.setObjectName("urun_sayisi")
            self.horizontalLayout.addWidget(self.urun_sayisi)
            self.onay_button = QPushButton("onay_button", self)
            self.onay_button.setObjectName("onay_button")
            self.horizontalLayout.addWidget(self.onay_button)
            self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
            self.urun_tablosu = QTableWidget(self)
            self.urun_tablosu.setObjectName("urun_tablosu")
            self.urun_tablosu.setColumnCount(2)
            self.urun_tablosu.setRowCount(0)
            self.urun_tablosu.setHorizontalHeaderLabels(["Ürün", "Fiyat"])
            self.urun_tablosu.setColumnWidth(0, 250)
            self.urun_tablosu.setColumnWidth(1, 79)
            self.gridLayout.addWidget(self.urun_tablosu, 0, 0, 1, 1)
        # SETTINGS
        self.new_tab_button.setEnabled(MainPage.settings.value("kategori_kullanimi"))

        # adding rows
        self.rowPosition = self.urun_tablosu.rowCount()
        self.urun_sayisi.valueChanged.connect(self.set_length)
        self.urun_tablosu.insertRow(self.rowPosition)
        self.onay_button.setAutoDefault(False)
        self.onay_button.clicked.connect(self.get_list)
        self.load_from_file_btn.clicked.connect(self.file_opener)

        self.onay_button.clicked.connect(MainPage.button_loader)

    def order_loader(self):
        fileName = MainPage.settings.value("items_cost_file_name")
        self.df_order = pd.read_csv(fileName, sep=";")
        self.row = 0
        self.urun_tablosu.setRowCount(len(self.df_order))
        self.urun_sayisi.setValue(len(self.df_order) - 1)
        for item, price in zip(self.df_order.Ürün, self.df_order.Fiyat):
            self.urun_tablosu.setItem(self.row, 0, QTableWidgetItem(str(item)))
            self.urun_tablosu.setItem(self.row, 1, QTableWidgetItem(str(price)))
            self.row += 1
        self.urun_tablosu.setRowCount(len(self.df_order))
        MainPage.button_loader()

    def file_opener(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*.csv);;CSV Files (*.csv)",
            options=options,
        )
        continue_use = yes_no_gen(
            self, message="Bu dosyayi daha sonra da kullanmak ister misiniz?"
        )
        MainPage.settings.setValue("continue_use_selected_csv", continue_use)
        if continue_use == 16384:
            MainPage.settings.setValue("items_cost_file_name", fileName)
        else:
            pass
        self.order_loader()

    def set_length(self):
        satir = self.urun_sayisi.value()
        self.urun_tablosu.setRowCount(int(satir))

    def get_list(self):
        # save point
        # self.urun_tablosu.setRowCount(0)
        try:
            self.items = item_list(
                [
                    self.urun_tablosu.item(i, 0).text()
                    for i in range(self.urun_tablosu.rowCount())
                ],
                [
                    self.urun_tablosu.item(i, 1).text()
                    for i in range(self.urun_tablosu.rowCount())
                ],
            )
            data = [
                i
                for i in map(
                    lambda x, y: [x, y], self.items.item_name, self.items.item_price
                )
            ]
            df_order = pd.DataFrame(data, columns=self.columns)

            df_order.to_csv("cost_2.csv", sep=";", index=False)
        except AttributeError:
            pop_up_gen(
                "There are empty rows inside the items, please try again after filling them!"
            )


def yes_no_gen(self, message="Var olan dosyadan yukelemek ister misiniz?", title=""):
    msg = QMessageBox.question(
        self,
        title,
        message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    return msg


def pop_up_gen(message, title="Uyari"):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setIcon(QMessageBox.Question)
    msg.setIcon(QMessageBox.Critical)
    msg.exec_()


class item_list:
    def __init__(self, item_name, item_price):
        self.item_name = item_name
        self.item_price = item_price


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
