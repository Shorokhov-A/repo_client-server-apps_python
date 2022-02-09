# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое
#    программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
#    Принудительно открыть файл в формате Unicode и вывести его содержимое.
from chardet import detect

with open('test_file.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(('сетевое программирование', 'сокет', 'декоратор', '')))

with open('test_file.txt', 'rb') as f:
    content = f.read()
encoding = detect(content)['encoding']

print('encoding: ', encoding)

with open('test_file.txt', encoding=encoding) as f_n:
    for line in f_n:
        print(line, end='')
