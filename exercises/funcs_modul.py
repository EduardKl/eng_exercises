import os
import re


PROJ_PATH = re.search(r'''([-\w\d\\/:.,'" ]+eng_exercises)''', os.path.abspath('.')).group(0)
EXERCS_PATH = os.path.join(PROJ_PATH, 'exercises')
print(os.path.join(EXERCS_PATH, 'connecting_modules.py'))


def get_exers_folders_names() -> list:
    """
    Функция собирает список названий папок в каталоге упражнений для последующего сбора модулей в функции get_moduls_to_importing.

    :return: Список названий папок, в которых содержаться модули упражнений.
    """

    exers_folders_names = [inner_entity for inner_entity in list(os.listdir(EXERCS_PATH)) if not re.search(r'__|\.py', inner_entity)]
    return exers_folders_names

def get_moduls_to_importing(exers_name_list: list) -> list:
    """
    Функция собирает список названий модулей для их импортирования в файле-коннекторе функцией generate_file_connector.

    :param exers_name_list: Список папок с упражнениями.
    :return: Список словарей с данными для импортирования.
    """
    moduls_list = []
    for exers_name in exers_name_list:
        for inner in os.listdir(os.path.join(EXERCS_PATH, exers_name)):
            if inner.find('.py') != -1:
                cls = inner[:-3]
                modul = f"exercises.{exers_name}.{cls}"
                moduls_list.append({
                    'modul': modul,
                    'cls': cls
                })
    return moduls_list

def generate_file_connector(moduls_list: list) -> None:
    """
    Функция создаёт файл, в котором импортируются все модули упражнений.
    В этом же файле собираются в общий список экземпляры всех модулей.

    :param moduls_list: список с названиями модулей для импортирования.
    :return: None
    """
    with open(os.path.join(EXERCS_PATH, 'connecting_modules.py'), 'w', encoding="utf-8") as PyFile:
        string = ''
        for modul in moduls_list:
            string += f"from {modul['modul']} import {modul['cls']}\n"
        string += '\n\n'

        string += 'exercises_list = []\n'
        for modul in moduls_list:
            element = "{" + f"'name': {modul['cls']}.__doc__, " + f"'class': {modul['cls']}" + "}"
            string += f"exercises_list.append({element})\n"

        PyFile.write(string)

def get_exerc() -> tuple:
    """
    Функция последовательным вызовом get_exers_folders_names, get_moduls_to_importing, generate_file_connector
    формирует файл с импортом всех модулей с упражнениями.
    Импортирует список с ссылками на классы упражнений из сгенерированного файла.

    :return: Список ссылок классов упражнений.
    """
    exers_folders_names = get_exers_folders_names()
    moduls_list = get_moduls_to_importing(exers_folders_names)
    generate_file_connector(moduls_list)

    from exercises.connecting_modules import exercises_list

    return tuple(exercises_list)
