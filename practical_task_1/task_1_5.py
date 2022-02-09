# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
#    байтовового в строковый тип на кириллице.
import chardet
import subprocess
import platform


def ping_stdout_print(arg):
    for line in arg.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


def ping_servers_print(*args, count=4):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    for arg in args:
        ping_command = ['ping', param, str(count), arg]
        subproc_ping = subprocess.Popen(ping_command, stdout=subprocess.PIPE)
        ping_stdout_print(subproc_ping)


yandex_domain = 'yandex.ru'
youtube_domain = 'youtube.com'

ping_servers_print(yandex_domain, youtube_domain)
