from Eng_Exercises_Bot import Eng_Excercises_Bot
from exercises import EXERCS_LIST


class Exercises(Eng_Excercises_Bot):
    """Контроллер упражнений для английского языка."""
    def __init__(self, exercises_tpl: tuple) -> None:
        """
        :param excercises_tpl: ({'name': Название упр, 'class': Ссылка на класс})
        """
        super().__init__()
        self.exercises_tpl = exercises_tpl

    def choice_exercises(self):
        """
        Функция выводит список упражнений из модуля exercises.
        :return: Экземпляр класса выбранного упражнения.
        """
        text_message = 'Список упражнений:\n'
        for i, exerc in enumerate(self.exercises_tpl, 1):
            text_message += f'\t{i}. {exerc["name"]}\n'

        self.send_message(text_message)
        choice = int(self.wait_answer()) - 1

        return self.exercises_tpl[choice]['class']()

    def start(self):
        exerc = self.choice_exercises()
        exerc.run()


if __name__ == '__main__':
    exerc = Exercises(EXERCS_LIST)
    exerc.start()





