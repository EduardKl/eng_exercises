import csv
import re
from os.path import abspath
import random
from pprint import pprint

ONE_PAGE = 20
TWO_PAGE = 40
THREE_PAGE = 60
FOUR_PAGE = 80


class Irregular_Verbs_Exc:
    """Упражнение на отработку неправильных глаголов."""
    def __init__(self, min_number=0, max_number=FOUR_PAGE):
        self.proj_path = re.search(r'''([-\w\d\\:.,'"]+eng_exercises)''', abspath('.')).group(0) + '\\'
        self.exerc_path = self.proj_path + 'exercises\\irregular_verbs\\'
        self.csv_file = self.exerc_path + 'irregular_verbs.csv'

        self.min_number = min_number
        self.max_number = max_number

    def get_verbs(self):
        with open(self.csv_file, 'r', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=['Translate', 'Base_Form', 'Past_Simple', 'Past_Participle'], delimiter=';')
            verbs_list = list(reader)
            verbs_list.pop(0)
        return verbs_list[self.min_number:self.max_number]



    def view_all_verbs(self):
        verbs_list = self.get_verbs()
        line_delim = f"|{'-' * 4}|{'-' * 20}|{'-' * 20}|{'-' * 20}|{'-' * 20}|\n"


        table_str = "{line_delim}|{0:^4}|{1:^20}|{2:^20}|{3:^20}|{4:^20}|\n{line_delim}".format('№', 'Translate', 'Base Form', 'Past Simple', 'Past Participle',
                                                                                                line_delim=line_delim)
        for i, verb in enumerate(verbs_list, 1):
            table_str += "|{num:^4}|{translate:^20}|{base_form:^20}|{past_simple:^20}|{past_participle:^20}|\n".format(
                num=i,
                translate=verb['Translate'],
                base_form=verb['Base_Form'],
                past_simple=verb['Past_Simple'],
                past_participle=verb['Past_Participle']
            )
            table_str += line_delim
        print(table_str)

    def irregular_verbs(self):
        verbs_list = self.get_verbs()
        
        while True:
            verb_dict = random.choice(verbs_list)
            print(f"{verb_dict['Translate']}:")
            bf_ans = input(f"Base -- ")
            if bf_ans == verb_dict['Base_Form']:
                print('+')
            else:
                print(f"- {verb_dict['Base_Form']}")

            ps_ans = input(f"Simple -- ")
            if bf_ans == verb_dict['Past_Simple']:
                print('+')
            else:
                print(f"- {verb_dict['Past_Simple']}")

            pp_ans = input(f"Participle -- ")
            if bf_ans == verb_dict['Past_Participle']:
                print('+')
            else:
                print(f"- {verb_dict['Past_Participle']}")
            print()


    def run(self):
        self.irregular_verbs()

if __name__ == '__main__':
    # with open('irregular_verbs.csv', 'r+', encoding='utf-8-sig') as csv_file:


    Irregular_Verbs_Exc(ONE_PAGE).view_all_verbs()
