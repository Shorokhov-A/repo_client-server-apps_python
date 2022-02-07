# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
#    последовательность кодов (не используя методы encode и decode) и определить тип,
#    содержимое и длину соответствующих переменных.
def strings_features_print(*strings):
    for item in strings:
        print(item, type(item), len(item))
    print('------------------------------')


bytes_string_1 = b'class'
bytes_string_2 = b'function'
bytes_string_3 = b'method'

strings_features_print(bytes_string_1, bytes_string_2, bytes_string_3)
