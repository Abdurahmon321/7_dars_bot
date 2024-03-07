import sqlite3


class DataBase:
    def __init__(self, path_to_db='main.db'):
        self.path_to_db = path_to_db

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = sqlite3.connect(self.path_to_db)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = """create table if not exists users(
            telegram_id INTEGER PRIMARY KEY,
            full_name VARCHAR(250),
            phone_number VARCHAR(13)
        )"""
        self.execute(sql, commit=True)

    def drop_table_users(self):
        sql = '''DROP TABLE IF EXISTS users'''
        self.execute(sql, commit=True)

    def insert_tg_id(self, tg_id):
        sql = """Insert into users(telegram_id) VALUES(?) on conflict do nothing"""
        self.execute(sql, parameters=(tg_id,), commit=True)

    def check_user(self, tg_id):
        sql = '''SELECT full_name, phone_number FROM users WHERE telegram_id = ?'''
        return self.execute(sql, parameters=(tg_id,), fetchone=True)

    def update_from_telegram_id(self, telegram_id, full_name, phone_number):
        sql = '''UPDATE users SET full_name = ?, phone_number = ? WHERE telegram_id = ?'''
        self.execute(sql, parameters=(full_name, phone_number, telegram_id), commit=True)
