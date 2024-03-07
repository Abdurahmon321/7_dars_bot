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

    def insert_tg_id(self, tg_id):
        sql = """Insert into users(telegram_id) VALUES(?) on conflict do nothing"""
        self.execute(sql, parameters=(tg_id,), commit=True)
