import sys
import json
import logging
import logs.server_log_config
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, \
    ERROR, DEFAULT_PORT, MAX_CONNECTIONS
from common.utils import get_message, send_message
from errors import IncorrectDataReceivedError

# Инициализация логирования сервера:
SERVER_LOGGER = logging.getLogger('server')


def process_client_message(message):
    """
    Обработчик сообщений от клиентов.
    Функция принимает словарь-сообщение от клиента, проверяет корректность, возвращает словарь-ответ для клиента.
    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {message}.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad request',
    }


def get_port():
    if '-p' in sys.argv:
        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        listen_port = DEFAULT_PORT
    if listen_port < 1024 or listen_port > 65535:
        SERVER_LOGGER.critical(
            f'Попытка запуска сервера с неподходящим номером порта: {listen_port}.'
            f' Допустимые адреса с 1024 до 65535. Клиент завершается.'
        )
        raise ValueError
    return listen_port


def get_address():
    if '-a' in sys.argv:
        listen_address = sys.argv[sys.argv.index('-a') + 1]
    else:
        listen_address = ''
    return listen_address


def main():
    """
    Загрузка параметров командной строки.
    Если нет параметров, то задаем значения по умолчанию.
    :return:
    """
    # Сначала обрабатываем порт: server.py -p 8888 -a 127.0.0.1
    try:
        listen_port = get_port()
    except IndexError:
        SERVER_LOGGER.error('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        sys.exit(1)

    # Затем обрабатываем адрес
    try:
        listen_address = get_address()
    except IndexError:
        SERVER_LOGGER.error('После параметра -\'a\' необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    SERVER_LOGGER.info(f'Запущен сервер. Порт для подключений: {listen_port}, '
                       f'адрес, с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, то принимаются соединения с любых адресов.')

    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}.')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать полученную Json строку, '
                                f'полученную от клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataReceivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
