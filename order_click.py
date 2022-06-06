def order_click(self):
    # get the name of button triggered this function
    ordered = self.sender()

    # todays date
    self.date = datetime.datetime.today().strftime("%d-%m-%Y")
    # algorithm that detects where to write current order
    # if there is no order today, means its first order 0001 and todays date
    if (self.date in self.df["date"].values) is False:
        self.new_row = {
            "date": str(self.date),
            "#": str("0001"),
            "orders": f"{ordered.text()}",
            "cost": 0,
        }
        self.df = self.df.append(self.new_row, ignore_index=True)
    else:  # if not first check
        if self.df["cost"].iloc[[-1]].values[0] == 0:
            self.df["orders"][self.df["#"] == self.order_id.text()] += [
                f",{ordered.text()}"
            ]
        else:
            self.new_row = {
                "date": str(self.date),
                "#": str(int(self.df["#"].iloc[[-1]]) + 1).zfill(4),
                "orders": f"{ordered.text()}",
                "cost": 0,
            }
        self.df = self.df.append(self.new_row, ignore_index=True)
    print(self.df)
    # self.load_order()
