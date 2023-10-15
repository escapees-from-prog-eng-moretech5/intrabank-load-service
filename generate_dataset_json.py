import random
import json

data = []

for _ in range(265*50):
    time = random.randint(8 * 60, 22 * 60)//30 * 30
    day = random.randint(1, 6)
    num_people = random.randint(0, 20)

    item = {
        "time": time,
        "day": day,
        "num_people": num_people
    }

    data.append(item)

with open('dataset.json', 'w') as json_file:
    json.dump(data, json_file)
