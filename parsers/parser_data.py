import re

with open('offices.txt', 'r', encoding='utf-8') as file:
    data = file.read()


def replace_days_status(text):
    text = re.sub(r'\Wпн', '"MONDAY', text)
    text = re.sub(r'\Wвт', '"TUESDAY', text)
    text = re.sub(r'\Wср', '"WEDNESDAY', text)
    text = re.sub(r'\Wчт', '"THURSDAY', text)
    text = re.sub(r'\Wпт', '"FRIDAY', text)
    text = re.sub(r'\Wсб', '"SATURDAY', text)
    text = re.sub(r'\Wвс', '"SUNDAY', text)
    text = re.sub(r'открытая', 'OPEN', text)
    text = re.sub(r'закрытая', 'CLOSED', text)
    text = re.sub(r'есть РКО', 'true', text)
    text = re.sub(r'нет РКО', 'false', text)
    text = re.sub(r'\WY', 'true', text)
    text = re.sub(r'\WN', 'false', text)
    text = re.sub(r'days', 'day', text)
    return text


def convert_to_format(match):
    time_str = match.group(0)
    time_str = time_str.strip(' "')
    if time_str == 'выходной':
        return time_str
    else:
        open_time, close_time = time_str.split('-')
        open_time = open_time.strip()
        close_time = close_time.strip()
        return f'open:"{convert_to_minutes(open_time)}", close:"{convert_to_minutes(close_time)}"'


def convert_to_minutes(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes


data = replace_days_status(data)
with open('offices_new.txt', 'w', encoding='utf-8') as file:
    file.write(data)


def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        data = input_file.read()

    off_pattern = r'\{\s*?"day":.*?\s*?"hours":\s*?"выходной"\s*?\},?'
    data = re.sub(off_pattern, '', data)

    def replacement(match):
        hours_minutes = re.findall(r'\d+', match.group(0))
        open_hours = int(hours_minutes[0]) * 60 + int(hours_minutes[1])
        close_hours = int(hours_minutes[2]) * 60 + int(hours_minutes[3])
        return f'"open": "{open_hours}",\n\t\t\t\t"close": "{close_hours}"'

    pattern = r'"hours": "\d{2}:\d{2}-\d{2}:\d{2}"'
    modified_data = re.sub(pattern, replacement, data)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(modified_data)


process_file('offices_new.txt', 'for_dima.txt')
