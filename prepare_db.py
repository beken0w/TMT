import os
import sqlite3
from dotenv import load_dotenv

FIXTERES = [
    ("Купить продукты", "Овощи, фрукты, хлеб"),
    ("Оплатить кварплату", "за Март"),
    ("Купить билет", "в Дубаи на Апрель"),
    ("Шашлыки", "Обзвонить друзей и собраться на шашлыки"),
    ("ТО машины", "Пройти ТО до Ноября"),
]

load_dotenv()

db_name = os.getenv('db_name', default="main.db")


def prepare_db(db_name):
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE tasks ( "
            "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
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
            cursor.execute("INSERT INTO tasks (title, description) VALUES(?, ?);",
                          (fixture[0], fixture[1]))
        connection.commit()
        print("Фикстуры занесены в таблицу")


if __name__ == '__main__':
    prepare_db(db_name)
    create_fixtures(db_name)