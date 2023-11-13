import re
import os
import csv
import random


class Prog_Words:
    """Отработка 100 английских слов для программистов."""
    def __init__(self):
        self.proj_path = re.search(r'''([-\w\d\\:.,'"]+eng_exercises)''', os.path.abspath('.')).group(0) + '\\'
        self.exerc_path = self.proj_path + 'exercises\\prog_words\\'
        self.csv_file = self.exerc_path + 'prog_words.csv'

    def get_words_csv(self):
        with open(self.csv_file, 'r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=['Word', 'Definition'], delimiter=';')
            words_list = list(reader)
            words_list.pop(0)
        return words_list


    def start(self):
        print('Выберите тип упражнения:\n'
              '\t1. Перевод на русский;\n'
              '\t2. Обратный перевод;\n')
        self.type = int(input('Введите номер: '))


    def run(self):
        # self.start()
        words_list = self.get_words_csv()

        while True:
            word = random.choice(words_list)

            # if self.type:
            quest = word['Word']

            index = word['Definition'].find('. ')
            ans = word['Definition'] if index == -1 else word['Definition'][:index]


            answer = input(f"{word['Word']} -- ")
            if not answer: break
            print('+') if answer == ans else print('-')
            print(f"{word['Word']} -- {word['Definition']}\n")
