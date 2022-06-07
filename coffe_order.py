import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
import pandas as pd
import datetime

# nan degerleri oldugu icin hata veriyor
# csv ye hemen date ve # eklenmemeli
# bunun icin bir yol bul!


class OrderPage(QDialog):
    def __init__(self):
        super().__init__()
        self.w = None
        loadUi("order.ui", self)

        self.order_id.setText(MainPage.df["#"].iloc[[-1]].values[0])

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

    def ok_(self):
        print("ok clicked")
        MainPage.df["cost"].mask(
            ((MainPage.df["#"] == 2) & (MainPage.df["date"] == MainPage.date)),
            self.total,
            inplace=True,
        )
        MainPage.df.to_csv("june.csv", sep=";", index=False)
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

        print(MainPage.df)
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
        #  populating tablewidget
        self.row = 0
        self.total = 0
        for order in current_order:
            self.tableWidget.setItem(self.row, 0, QTableWidgetItem(str(order)))
            new_cost = self.cost_df["cost"][self.cost_df["products"] == order].values[0]
            self.total += int(new_cost)

            self.tableWidget.setItem(self.row, 1, QTableWidgetItem(str(new_cost)))
            self.check.setText(str(self.total))
            self.row += 1


class MainPage(QDialog):
    def __init__(self):
        super().__init__()
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})
        self.w = None
        loadUi("MainPage.ui", self)
        self.siparisgir.clicked.connect(self.new_order)

    def new_order(self):
        # reading saves of customer orders
        # converting customer order_id into string, we want 0001 not 1
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})
        # todays date
        self.date = datetime.datetime.today().strftime("%d-%m-%Y")
        # creating customer id in 0000 format then changing label to it

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
        if self.w is None:
            self.w = OrderPage()
        self.w.show()

    def save_csv(self):
        # saving orders into csv with given orders and total cost info
        self.df.to_csv("june.csv", sep=";", index=False)


app = QApplication(sys.argv)
MainPage = MainPage()
MainPage.show()
sys.exit(app.exec_())
