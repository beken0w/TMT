import os
import sqlite3
from dotenv import load_dotenv


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


if __name__ == '__main__':
    prepare_db(db_name)
