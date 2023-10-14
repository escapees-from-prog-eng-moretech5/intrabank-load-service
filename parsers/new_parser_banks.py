import re


def days_in_interval(day1, day2):
    days_order = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    index1 = days_order.index(day1)
    index2 = days_order.index(day2)
    if index1 > index2:
        index1, index2 = index2, index1

    interval_days = days_order[index1:index2 + 1]

    return interval_days


def transform_structure(structure_list):

    new_structure = []

    for structure in structure_list:
        matched_days = re.findall(r'"(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)"', structure["day"])

        if len(matched_days) == 2:
            _, interval_days = days_in_interval(matched_days[0].capitalize(), matched_days[1].capitalize())

            for day in interval_days:
                new_structure.append({
                    "day": day.upper(),
                    "open": structure["open"],
                    "close": structure["close"]
                })
        elif len(matched_days) == 1:
            new_structure.append({
                "day": matched_days[0],
                "open": structure["open"],
                "close": structure["close"]
            })

    return new_structure

transformed_data = transform_structure(test_data)
transformed_data
