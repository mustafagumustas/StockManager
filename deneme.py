import pandas as pd
import datetime
import numpy as np

# print(datetime.datetime.today().strftime("%d-%m-%Y"))

df = pd.read_csv("june.csv", sep=";")

# new_df = pd.DataFrame(columns=["date", "#", "orders", "cost"])
date = datetime.datetime.today().strftime("%d-%m-%Y")
new_customer_id = str(int(df["#"].iloc[[-1]]) + 1).zfill(4)

# print(df)

new_df = pd.DataFrame(
    {
        "date": [str(date)],
        "#": [new_customer_id],
        "orders": "Filter Coffee",
        "cost": [0],
    }
)

cond = (df["date"] == date) & (df["#"] == new_customer_id)

df = pd.concat([df, new_df], ignore_index=True, axis=0,)
print(df.loc[(df["date"] == date) & (df["#"] == new_customer_id)])
df.loc[((df["date"] == date) & (df["#"] == new_customer_id)), "cost"] = 90
last_order = list(
    df["orders"].loc[((df["date"] == date) & (df["#"] == new_customer_id))].values
)

last_order.append("Espresso")
df.loc[((df["date"] == date) & (df["#"] == new_customer_id)), "orders"] = ",".join(
    last_order
)
last_order.append("Espresso")
df.loc[((df["date"] == date) & (df["#"] == new_customer_id)), "orders"] = ",".join(
    last_order
)
print(df)
