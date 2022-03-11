import sys
import json
import logging
import argparse
import select
import time
import logs.server_log_config
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, \
    MESSAGE, MESSAGE_TEXT, ERROR, DEFAULT_PORT, MAX_CONNECTIONS, SENDER
from common.utils import get_message, send_message
from decorators import log

# Инициализация логирования сервера:
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages_list, client):
    """
    Обработчик сообщений от клиентов.
    Функция принимает словарь-сообщение от клиента, проверяет корректность, возвращает словарь-ответ для клиента.
    :param message:
    :param messages_list:
    :param client:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента: {message}.')
    # Если это сообщение присутствует, принимаем и отвечаем.
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
            and MESSAGE_TEXT in message:
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad request',
        })
        return


@log
def arg_parser():
    """Парсер аргументов командной строки."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # Проверка получения корректного номера порта для работы сервера.
    if not 1023 < listen_port < 65535:
        SERVER_LOGGER.critical(
            f'Попытка запуска сервера с неподходящим номером порта: {listen_port}.'
            f' Допустимые адреса с 1024 до 65535. Клиент завершается.'
        )
        sys.exit(1)

    return listen_address, listen_port


def main():
    """
    Загрузка параметров командной строки.
    Если нет параметров, то задаем значения по умолчанию.
    :return:
    """
    listen_address, listen_port = arg_parser()

    SERVER_LOGGER.info(f'Запущен сервер. Порт для подключений: {listen_port}, '
                       f'адрес, с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, то принимаются соединения с любых адресов.')

    # Готовим сокет.
    transport = socket(AF_INET, SOCK_STREAM)
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))
    transport.settimeout(1)

    # Список клиентов, очередь сообщений.
    clients = []
    messages = []

    # Слушаем порт.
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno)
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК {client_address}.')
            clients.append(client)

        recv_data_list = []
        send_data_list = []
        err_list = []

        # Проверяем на наличие ждущих клиентов.
        try:
            if clients:
                recv_data_list, send_data_list, err_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        # Принимаем сообщения и еcли они есть, то кладем в словарь. В случае ошибки исключаем клиента.
        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)
        # Если есть сообщения для отправки и ожидающие клиенты, то отправляем им сообщение.
        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
