import pandas as pd


class User:
    yandexToken = ''

    def __init__(self, token):
        self.yandexToken = token


class Database:

    def __init__(self):
        self.table = pd.Series(dict())

    def add_user(self, user_id, token):
        self.table[user_id] = User(token)

    def get_user_data(self, user_id):
        return self.table[user_id]
