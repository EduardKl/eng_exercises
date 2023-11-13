from typing import Dict
from Eng_Exercises_Bot import Eng_Excercises_Bot
import random
import os
import csv
import re

class Word_Trans_Exerc(Eng_Excercises_Bot):
    'Упражнение вида "слово -- перевод".'
    def __init__(self) -> None:
        "При инициализации экземпляра класса происходит сохранение необходимых для работы упражнения путей."
        super().__init__()
        self.proj_path = re.search(r'''([-\w\d\\/:.,'" ]+eng_exercises)''', os.path.abspath('.')).group(0)
        self.exerc_path = os.path.join(self.proj_path, 'exercises', 'word_trans_exerc')
        self.dicts_path = os.path.join(self.exerc_path, 'dictionaries')


    def chenge_type(self) -> None:
        # Функция меняет тип упражнения
        # 0 -- писать перевод на русском
        # 1 -- писать обратный перевод на английский
        if self.type: self.type = 0
        else: self.type = 1
        self.send_message('Тип изменён')
    

    def get_groups(self, group: str = '') -> Dict:
        """
        Функция проходит по каждому файлу из каталога для словарей.
        return: Словарь вида {'folders': [список названий папок в указанном каталоге], 'file': [список названий файлов в указанном каталоге]}
        """
        dict_names = {'folders': [], 'files': []}
        if not group: group = self.dicts_path
        for inner_entity in os.listdir(group):
            inner_path = os.path.join(group, inner_entity)
            if (os.path.isdir(inner_path)):
                dict_names['folders'].append(inner_entity)
            elif (os.path.isfile(inner_path)):
                dict_names['files'].append(inner_entity[:-4])
        return dict_names
    def choice_dict(self):
        # Выводит в консоль пронумированный список словарей из папки dictionaries.
        # Возвращает название файла выбранного словаря.
        """
        Выводит список.
        При выборе либо возвращает выбранный словарь, либо выводит содержимое выбранной группы.
        """
        dict_path = self.dicts_path
        while True:
            if 'dict_names' not in locals():
                dict_names = self.get_groups()
            else:
                if choice <= i - 1:
                    choice_folder = dict_names['folders'][choice]
                    dict_path = os.path.join(dict_path, choice_folder)
                    dict_names = self.get_groups(dict_path)
                else:
                    dict_path = os.path.join(dict_path, dict_names['files'][choice])
                    return dict_path
                i = 0  # Обнуляю значение счетчика на случай, при котором в выбранной группе нет папок.

            text_message = ''
            if dict_names['folders']:
                text_message += 'Выберите группу:\n'
                for i, group_name in enumerate(dict_names['folders'], 1):
                    text_message += f'{i}. {group_name}\n'
                
            if dict_names['files']:
                text_message += 'Выберите словарь:\n'
                for k, dict_name in enumerate(dict_names['files'], i + 1):
                    text_message += f'{k}. {dict_name}\n'

            self.send_message(text_message)
            choice = int(self.wait_answer()) - 1
        
        

    def get_dict(self, dict_path) -> list:
        "Функция перебирает файл выбранного словаря и записывает все слова в список кортежей."
        dictionary = []
        with open(dict_path+'.csv', 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for i, line in enumerate(csv_reader):
                if not i: continue
                if line:
                    eng = line['eng'].strip().lower()
                    rus = line['rus'].strip().lower()
                    if rus.find(',') != -1:
                        rus = [word.strip() for word in rus.split(',')]

                    dictionary.append((eng, rus))
        return dictionary


    def start(self):
        self.send_message('Выберите тип упражнения:\n'
              '1. Перевод на русский;\n'
              '2. Обратный перевод;\n')
        self.type = int(self.wait_answer())

    def translating(self):
        while True:
            # Выбор и загрузка словаря, при запуске программы или смене тематики.
            if ('answer' not in locals()) or (answer == 2):
                dict_path = self.choice_dict()
                dictionary = self.get_dict(dict_path)
                random.shuffle(dictionary)

            # Получение случайного слова из списка
            word_tuple = random.choice(dictionary)
            eng = word_tuple[0]
            rus = word_tuple[1]
            if self.type == 1:
                question = eng
                translation = rus
            else:
                question = random.choice(rus) if isinstance(rus, list) else rus
                translation = eng


            # Вопрос, получение ответа.
            self.send_message(question)
            answer = self.wait_answer()
            if answer.isdigit(): answer = int(answer)
            if not answer: break
            if answer == 1: 
                self.chenge_type()
                continue
            if answer == 2: continue

            # Проверка введённого значения
            if self.type == 1:
                if (isinstance(rus, list) and answer in rus) or (answer == rus):
                    self.send_message('+')
                else:
                    self.send_message(f'Нет, {rus}.')
            else:
                if answer == eng:
                    self.send_message('+')
                else:
                    self.send_message(f'No, {eng}.')


    def run(self):
        self.start()
        self.translating()


if __name__ == '__main__':
    obj = Word_Trans_Exerc()
    obj.run()