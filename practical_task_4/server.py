import sys
import json
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, RESPONSE_DEFAULT_IP_ADDRESS, \
    ERROR, DEFAULT_PORT, MAX_CONNECTIONS
from common.utils import get_message, send_message


def process_client_message(message):
    """
    Обработчик сообщений от клиентов.
    Функция принимает словарь-сообщение от клиента, проверяет корректность, возвращает словарь-ответ для клиента.
    :param message:
    :return:
    """
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE_DEFAULT_IP_ADDRESS: 400,
        ERROR: 'Bad request',
    }


def get_port():
    if '-p' in sys.argv:
        listen_port = int(sys.argv[sys.argv.index('-p') + 1])
    else:
        listen_port = DEFAULT_PORT
    if listen_port < 1024 or listen_port > 65535:
        raise ValueError
    return listen_port


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
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('В качестве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем обрабатываем адрес
    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''
    except IndexError:
        print('После параметра -\'a\' необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
