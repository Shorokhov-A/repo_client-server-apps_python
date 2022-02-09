# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
#    проверить тип и содержание соответствующих переменных. Затем с помощью
#    онлайн-конвертера преобразовать строковые представление в формат Unicode и также
#    проверить тип и содержимое переменных.

def words_type_print(*words):
    for item in words:
        print(item, type(item))
    print('----------------------------')


first_word = 'разработка'
second_word = 'сокет'
third_word = 'декоратор'

words_type_print(first_word, second_word, third_word)

first_word_unicode = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
second_word_unicode = '\u0441\u043e\u043a\u0435\u0442'
third_word_unicode = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

words_type_print(first_word_unicode, second_word_unicode, third_word_unicode)
