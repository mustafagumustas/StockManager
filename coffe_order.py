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
        self.row = 0
        # reading saves of customer orders
        # converting customer order_id into string, we want 0001 not 1
        self.df = pd.read_csv("june.csv", sep=";", converters={"#": lambda x: str(x)})

        # creating customer id in 0000 format then changing label to it
        self.new_customer_id = str(int(self.df["#"].iloc[[-1]]) + 1).zfill(4)
        self.order_id.setText(self.new_customer_id)

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

        self.total = 0
        self.ok_button.clicked.connect(self.ok_)

    def ok_(self):
        self.df["cost"].mask(
            ((self.df["#"] == 2) & (self.df["date"] == self.date)),
            self.total,
            inplace=True,
        )
        MainPage.save_csv()
        self.close

    def order_click(self):
        # get the name of button triggered this function
        ordered = self.sender()

        # todays date
        self.date = datetime.datetime.today().strftime("%d-%m-%Y")
        # algorithm that detects where to write current order
        # if there is no order today, means its first order 0001 and todays date
        if (self.date in self.df["date"].values) is False:
            new_df = pd.DataFrame(
                {
                    "date": [str(self.date)],
                    "#": ["0001"],
                    "orders": f"{ordered.text()}",
                    "cost": [0],
                }
            )
            self.df = pd.concat([self.df, new_df], ignore_index=True, axis=0)
        else:  # if not first check
            if self.df["cost"].iloc[[-1]].values[0] == 0:
                last_order = list(
                    self.df["orders"]
                    .loc[
                        (
                            (self.df["date"] == self.date)
                            & (self.df["#"] == self.new_customer_id)
                        )
                    ]
                    .values
                )
                last_order.append(f"{ordered.text()}")
                self.df.loc[
                    (
                        (self.df["date"] == self.date)
                        & (self.df["#"] == self.new_customer_id)
                    ),
                    "orders",
                ] = ",".join(last_order)
            else:
                new_df = pd.DataFrame(
                    {
                        "date": [str(self.date)],
                        "#": [self.new_customer_id],
                        "orders": [ordered.text()],
                        "cost": [0],
                    }
                )
                self.df = pd.concat([self.df, new_df], ignore_index=True, axis=0,)
        print(self.df)
        self.load_order()

    def load_order(self):
        print(self.row)
        # getting orders from df
        current_order = (
            self.df["orders"][self.df["#"] == self.order_id.text()]
            .to_list()[0]
            .split(",")
        )
        self.tableWidget.setRowCount(len(current_order))
        #  populating tablewidget
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
