import pandas as pd
import random
from datetime import datetime, timedelta

days_in_month = 31
times = [10, 15, 17, 19, 21]
days_of_week = [1, 2, 3, 4, 5, 6, 7]

data = []

for day in range(1, days_in_month + 1):
    for time in times:
        for day_of_week in days_of_week:
            visitors = random.randint(8, 30)
            date_str = f"2023-10-{day:02d} {time}"
            data.append({"date": 1, "day_of_the_week": day_of_week, "time": time, "time_in_quee": visitors})


csv_columns = ["date", "day_of_the_week", "time", "customers"]

df = pd.DataFrame(data)

csv_file = "customers.csv"
df.to_csv(csv_file, index=False)

new = pd.read_csv(csv_file)
print(new.head(5))
