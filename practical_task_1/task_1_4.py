# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
#    строкового представления в байтовое и выполнить обратное преобразование (используя
#    методы encode и decode).
def encode_str_to_bytes(*args):
    result = []
    for arg in args:
        result.append(arg.encode('utf-8'))
    return result


def decode_bytes_to_str(*args):
    result = []
    for arg in args:
        result.append(arg.decode('utf-8'))
    return result


string_1 = 'разработка'
string_2 = 'администрирование'
string_3 = 'protocol'
string_4 = 'standard'

encode_str_list = encode_str_to_bytes(string_1, string_2, string_3, string_4)

print(*encode_str_list, sep='\n', end='\n---------------------\n')

decode_str_list = decode_bytes_to_str(*encode_str_list)

print(*decode_str_list, sep='\n')
