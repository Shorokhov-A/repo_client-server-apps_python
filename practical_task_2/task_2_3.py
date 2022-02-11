"""
3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
YAML-формата. Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке
ASCII (например, €);
Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла с
помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
import yaml

first_el = ['item_1', 'item_2', 'item_3']
second_el = 51
third_el = {
    'first_key': '€15',
    'second_key': '£39',
    'third_key': '¥71'
}

data_to_yaml = {
    'first_el': first_el,
    'second_el': second_el,
    'third_el': third_el
}

with open('result.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data_to_yaml, f, default_flow_style=False, allow_unicode=True)

with open('result.yaml', encoding='utf-8') as f:
    f_content = yaml.load(f, Loader=yaml.FullLoader)

print(data_to_yaml)
print(f_content)
print(data_to_yaml == f_content)
