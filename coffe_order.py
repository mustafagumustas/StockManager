import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
import pandas as pd
import datetime

# nan degerleri oldugu icin hata veriyor
# csv ye hemen date ve # eklenmemeli
# bunun icin bir yol bul!


class Stock_Editor:
    def __init__(self):
        super().__init__()
        self.w = None
        loadUi("stok.ui", self)
        rowPosition = self.table.rowCount()
        self.add_product.clicked.connect(self.add_row)

    def add_row(self):
        self.tableWidget.insertRow(self.rowPosition)


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
        self.cancel_button.clicked.connect(self.closeEvent)

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

    def closeEvent(self):
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
        self.siparisgoruntule.clicked(print("hey"))

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
        self.openWin()

    def openWin(self):
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
