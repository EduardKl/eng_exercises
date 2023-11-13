import requests
import environ
import os
import re


class Eng_Excercises_Bot:
    "Класс для взаимодействия с Telegram-ботом приложения."
    def __init__(self):
        "Инициализация экземпляра класса."
        proj_path = re.search(r'''([-\w\d\\/:.,'" ]+eng_exercises)''', os.path.abspath('.')).group(0)
        
        env = environ.Env(DEBUG = (bool, False))
        env.read_env(os.path.join(proj_path, 'config', '.env'))

        self.token = env('TOKEN')
        
    def send_message(self, message: str, chat_id: int = 1520870774):
        """
        Функция для отправки сообщения.
        """
        updates_list = requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={chat_id}&text={message}')
    def get_updates(self, last_update_id: int = 0):
        "Функци для получения необработанных изменений в чате."
        updates_resp = requests.get(f'https://api.telegram.org/bot{self.token}/getUpdates?offset={last_update_id}')
        return updates_resp.json()['result']
    def get_id_last_update(self):
        "Функция возвращает id последнего сообщения пользователя."
        updates_list = self.get_updates()
        if updates_list:
            return int(updates_list.pop()['update_id']) + 1
        else:
            return 0

    
    def wait_answer(self, last_update_id: int = 0):
        "Функция ожидает сообщение от пользователя и возвращает его при получении."
        last_update_id = self.get_id_last_update()
        while True:
            updates_list = self.get_updates(last_update_id)
            print(updates_list)
            if updates_list: return updates_list[0]['message']['text']

        