# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
#    байтовом типе.

def word_check(word):
    for letter in word:
        if ord(letter) > 127:
            print(f'Слово "{word}" невозможно записать в байтовом типе.')
            return
    print(f'Слово "{word}" можно записать в байтовом типе.')


def strings_to_byte_check(*words):
    for word in words:
        word_check(word)


string_1 = 'attribute'
string_2 = 'класс'
string_3 = 'функция'
string_4 = 'type'

strings_to_byte_check(string_1, string_2, string_3, string_4)
