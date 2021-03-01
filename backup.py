import os
import shutil

FROM_DIR = r'F:\Programming\Tasks\server_directory'  # прописываем путь к исходной директории
TO_DIR = r'F:\Programming\Tasks\new_directory'  # прописываем путь к директории в котрую будем копировать файлы
max_size = 3882000  # прописываем максимальный размер (в байтах) исходной директории, при котором копирование производиться не будет
exclusion_name = 'snccntx'


def folder_size(path: str) -> int:
    """функция считает размер папки, путь к папке передается в качестве аргумента"""

    total = 0  # счетчик общего размера папки
    for entry in os.scandir(path):  # функция scandir() - итератор, перебирает все объекты в директории
        if entry.is_file():  # is_file() объекта os.DirEntry используется для проверки, является ли запись файлом или нет
            total += entry.stat().st_size  # функция stat() модуля os получает статистическую информацию файла. атрибут st_size – размер файла в байтах
        elif entry.is_dir():  # is_dir() объекта os.DirEntry используется для проверки, является ли запись директорией или нет
            total += folder_size(entry.path)  # рикурсивно вызываем фуекцию, в качестве аргумента передаем поддиректорию
    return total  # возвращаем общий размер папки


def backup_dir(src: str = FROM_DIR, dst: str = TO_DIR) -> None:
    """функция копирует файлы из директриий, путь к которой передан в качестве первого аргумента
    в директрию, путь к которой передан в качестве второго аргумента"""

    for root, dirs, files in os.walk(src, topdown=False):  # Функция walk() модуля os генерирует имена файлов в дереве каталогов, обходя дерево сверху вниз или снизу вверх
        for name in dirs:  # перебираем циклом все имена вложенных папок
            if exclusion_name not in name:  # если имя папки не начинается с 'snccntx', то
                shutil.copytree(f'{src}\\{name}', f'{dst}\\{name}', dirs_exist_ok=True)  # метод copytree модуля shutil копирует файлы из директории(аргумент 1) в директорию(аргумент2) dirs_exist_ok=True - блокирует ошибку, если директория(аргумент 2) уже существует


def delete_copied_files(path: str = FROM_DIR) -> None:
    """функция удаляет все папки из директории, за исключением директории,
    имя которой начинается с символов, записанных в перееменной exclusion_name"""

    for root, dirs, files in os.walk(path, topdown=False):  # функция walk() модуля os генерирует имена файлов в дереве каталогов, обходя дерево сверху вниз или снизу вверх
        for name in dirs:  # перебираем циклом все имена вложенных папок
            if exclusion_name not in name: # если имя папки не начинается с 'snccntx', то
                shutil.rmtree(f'{path}\\{name}')  # метод rmtree(path) модуля shutil - удаляет текущую директорию и все поддиректории


if folder_size(FROM_DIR) > max_size:
    backup_dir(FROM_DIR, TO_DIR)
    delete_copied_files(FROM_DIR)
