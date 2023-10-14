import json


def parse_atm_data(data):
    parsed_data = []
    for atm_info in data["atms"]:
        atm_services = []
        for service, details in atm_info["services"].items():
            service_info = {
                "service": service,
                "capability": details["serviceCapability"],
                "activity": details["serviceActivity"]
            }
            atm_services.append(service_info)

        parsed_atm_info = {
            "address": atm_info["address"],
            "latitude": atm_info["latitude"],
            "longitude": atm_info["longitude"],
            "allDay": atm_info["allDay"],
            "services": atm_services
        }

        parsed_data.append(parsed_atm_info)
    return parsed_data


with open('atms.txt', 'r', encoding='utf-8') as file:
    atm_data = json.load(file)

parsed_data = parse_atm_data(atm_data)

with open('parsed_atm_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(parsed_data, json_file, indent=4)

print("Данные успешно сохранены в файл 'parsed_atm_data.json'")
