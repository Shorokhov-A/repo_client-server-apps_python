"""Ошибки"""


class IncorrectDataReceivedError(Exception):
    """
    Ошибка - от сокета получены некорректные данные.
    """
    def __str__(self):
        return 'Принято некорректное сообщение от удаленного компьютера.'


class ReqFieldMissingError(Exception):
    """
    Ошибка - отсутствует обязательное поле в принятом словаре.
    """
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В принятом словаре отсутствует обязательное поле {self.missing_field}.'
