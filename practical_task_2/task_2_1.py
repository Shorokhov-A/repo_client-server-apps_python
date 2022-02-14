"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции
создать главный список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета
в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих столбцов также
оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""
import re
import csv
from chardet import detect


def get_data():
    source_files = (
        'info_1.txt',
        'info_2.txt',
        'info_3.txt',
    )
    re_os_prod = re.compile(r'(?=Изготовитель системы:\s*(.+\S))')
    re_os_name = re.compile(r'(?=Название ОС:\s*(.+\S))')
    re_os_code = re.compile(r'(?=Код продукта:\s*(.+\S))')
    re_os_type = re.compile(r'(?=Тип системы:\s*(.+\S))')
    data_string = ''
    main_data = [
        [
            'Изготовитель системы',
            'Название ОС',
            'Код продукта',
            'Тип системы',
        ]
    ]
    for file in source_files:
        with open(file, 'rb') as f:
            content = f.read()
        encoding = detect(content)['encoding']
        with open(file, encoding=encoding) as f:
            data_string += ''.join((f.read(), '\n'))
    os_prod_list = re_os_prod.findall(data_string)
    os_name_list = re_os_name.findall(data_string)
    os_code_list = re_os_code.findall(data_string)
    os_type_list = re_os_type.findall(data_string)
    for os_prod, os_name, os_code, os_type in zip(os_prod_list, os_name_list, os_code_list, os_type_list):
        main_data.append([os_prod, os_name, os_code, os_type])
    return main_data


def write_to_csv(file_name: str) -> None:
    data = get_data()
    with open(file_name, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f)
        f_writer.writerows(data)


if __name__ == '__main__':
    write_to_csv('result.csv')
