"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. Написать
скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""
import json
from chardet import detect


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date: str):
    dict_to_json = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    with open('orders.json', 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']
    with open('orders.json', encoding=encoding) as f:
        f_content = json.load(f)
    f_content['orders'].append(dict_to_json)
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(f_content, f, indent=4)


if __name__ == '__main__':
    write_order_to_json('Рюкзак', 1, 2999.90, 'Покупатель', '11.02.2022')
