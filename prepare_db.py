import os
import sqlite3
from dotenv import load_dotenv

FIXTERES = [
    ("5724849259", "Купить продукты", "Овощи, фрукты, хлеб"),
    ("5724849259", "Оплатить кварплату", "за Март"),
    ("5724849259", "Купить билет", "в Дубаи на Апрель"),
    ("5724849259", "Шашлыки", "Обзвонить друзей и собраться на шашлыки"),
    ("5724849259", "ТО машины", "Пройти ТО до Ноября"),
]

load_dotenv()

db_name = os.getenv('db_name', default="main.db")


def prepare_db(db_name):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE tasks2 ( "
            "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
            "user_id INTEGER NOT NULL, "
            "title TEXT NOT NULL, "
            "description TEXT NOT NULL, "
            "status INTEGER NOT NULL DEFAULT (0));"
        )
        connection.commit()
        print("Таблица Tasks успешно создана")


def create_fixtures(db_name):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        for fixture in FIXTERES:
            cursor.execute("INSERT INTO tasks2 (user_id, title, description) VALUES(?, ?, ?);",
                           (fixture[0], fixture[1], fixture[2]))
        connection.commit()
        print("Фикстуры занесены в таблицу")


if __name__ == '__main__':
    prepare_db(db_name)
    create_fixtures(db_name)
