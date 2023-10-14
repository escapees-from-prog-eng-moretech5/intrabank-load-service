import pandas as pd
import random
from datetime import datetime, timedelta

days_in_month = 31
times = ["10:00", "15:00", "17:00", "19:00", "21:00"]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

data = []

for day in range(1, days_in_month + 1):
    for time in times:
        for day_of_week in days_of_week:
            visitors = random.randint(2, 30)
            date_str = f"2023-10-{day:02d} {time}"
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            data.append({"date": date, "day_of_the_week": day_of_week, "time": time, "time_in_quee": visitors})


csv_columns = ["date", "day_of_the_week", "time", "customers"]

df = pd.DataFrame(data)

csv_file = "customers.csv"
df.to_csv(csv_file, index=False)

new = pd.read_csv(csv_file)
print(new.head(5))
