import socket
import shutil
import os
from pathlib import Path

PORT = 9090
HOME = Path(Path.cwd(), 'home') #папка home

def _main():
    if not HOME.is_dir():
        mkdir(HOME)
    os.chdir(HOME)
    with socket.socket() as sock:
        sock.bind(('', PORT))
        sock.listen()
        print("Порт: ", PORT)

        while True:
            conn, addr = sock.accept()
            handle(conn)

def ls(path=None): #показывает содержимое папки
    if path:
        return '; '.join(os.listdir(path))
    return '; '.join(os.listdir(HOME))

def pwd(): #путь к текущей папке
    return str(HOME)

def mkdir(path): #создание папки
    path = Path(path)
    rm(path)
    path.mkdir(parents=True)

def touch(path, text=''): #создание пустого файла или сразу файла с текстом
    path = Path(path)
    path.touch()
    path.write_text(text)

def rm(path): #удаление файла
    path = Path(path)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.is_file():
        path.unlink()

def mv(src_path, dst_path): #перемещение файла
    src_path = Path(src_path)
    dst_path = Path(dst_path)
    if src_path.exists():
        shutil.move(src_path, dst_path)

def cat(path): #смотрим содержимое файла
    path = Path(path)
    if path.is_file():
        return path.read_text()

def help(): #выводит справку
    return 'help - выводит справку по командам\n' \
           'pwd - выводит путь текущего каталога\n' \
           'touch FILE [TEXT] - создает пустой файл или файл с текстом\n' \
           'cat FILE - выводит содержимое файла\n' \
           'rm FILE - удаляет файл\n' \
           'ls [DIRECTORY]- выводит содержимое каталога\n' \
           'mkdir DIRECTORY - создает каталог\n' \
           'mv SOURCE DESTINATION - перемещает (переименовывает файл)\n' \
           'exit - разрыв соединения с сервером'

def process(request): #запуск команд
    command, *args = request.split()
    commands = {
        'ls': ls,
        'pwd': pwd,
        'mkdir': mkdir,
        'touch': touch,
        'rm': rm,
        'mv': mv,
        'cat': cat,
        'help': help
    }
    try:
        return commands[command](*args)
    except (TypeError, KeyError):
        return 'Bad request'

def handle(conn):
    with conn:
        request = conn.recv(1024).decode()
        print(request)
        response = process(request)
        if response is None:
            response = ''
        conn.send(response.encode())

if __name__ == '__main__':
    _main()
