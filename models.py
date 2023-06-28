import os
import logging
import sqlite3

from dotenv import load_dotenv


load_dotenv()

db_name = os.getenv('db_name', default="main.db")

logging.basicConfig(level=logging.INFO,
                    filename='log_file.log',
                    filemode='a')


class Task:

    def add_value(self, name, value):
        setattr(self, name, value)

    def __beautify_response(self, rows):
        statuses = []
        ids = []
        result = []
        for row in rows:
            ids.append(row[0])
            statuses.append(row[4])
            result.append(
                f"{' '*40}Задача №{row[0]}\n\n"
                f"Заголовок: {row[2]}\n"
                f"Описание: {row[3]}\n"
                f"Статус: {'💼 Не выполнена' if row[4] == 0 else '✅ Выполнена'}"
            )
        return ids, statuses, result

    def __connect_to_db(self):
        if os.path.isfile(db_name):
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                logging.info("Connection successful!")
                return conn, cursor
            except Exception as e:
                raise Exception(
                    f"Возникли проблемы с подключением к базе:\n{e}")
        else:
            raise Exception("Отсутствует файл базы данных")

    def __disconnect_from_db(self, conn):
        conn.commit()
        conn.close()
        logging.info("Connection disconnected!")

    def is_exist(self, id):
        conn, cursor = self.__connect_to_db()
        logging.info("Проверяем существует ли запись с данным id")
        cursor.execute('SELECT count(*) from tasks2 where id = ?;', (id,))
        result = cursor.fetchone()
        self.__disconnect_from_db(conn)
        return result

    def has_permission(self, id, user_id):
        conn, cursor = self.__connect_to_db()
        logging.info("Проверяем существует ли запись сданным id")
        cursor.execute('SELECT count(*) from tasks2 where id = ? and user_id = ?;', (id, user_id))
        result = cursor.fetchone()
        self.__disconnect_from_db(conn)
        return result

    def check_status(self, id):
        conn, cursor = self.__connect_to_db()
        logging.info("Проверяем статус записи с данным id")
        cursor.execute('SELECT status from tasks2 where id = ?;', (id,))
        result = cursor.fetchone()
        self.__disconnect_from_db(conn)
        return result

    def get_created_task(self):
        conn, cursor = self.__connect_to_db()
        logging.info("Извлекаем из базы новую запись")
        cursor.execute('select * from tasks2 order by id desc limit 1;')
        text = self.__beautify_response(cursor.fetchall())
        self.__disconnect_from_db(conn)
        return text

    def select_tasks(self, user_id):
        conn, cursor = self.__connect_to_db()
        logging.info("Извлекаем из базы все записи")
        cursor.execute('SELECT * from tasks2 where user_id = ?', (user_id,))
        text = self.__beautify_response(cursor.fetchall())
        self.__disconnect_from_db(conn)
        return text

    def insert_task(self, user_id):
        conn, cursor = self.__connect_to_db()
        logging.info("Создаем запись в базе")
        cursor.execute('INSERT INTO tasks2 (user_id, title, description) VALUES(?, ?, ?);',
                       (user_id, self.title, self.description))
        self.__disconnect_from_db(conn)

    def update_status(self, id):
        conn, cursor = self.__connect_to_db()
        logging.info("Обновляем статус записи с данным id")
        cursor.execute('update tasks2 set status = 1 where id = ?;', (id,))
        self.__disconnect_from_db(conn)

    def delete_task(self, id):
        conn, cursor = self.__connect_to_db()
        logging.info("Удаляем запись из базы")
        cursor.execute('delete from tasks2 where id = ?;', (id,))
        self.__disconnect_from_db(conn)


class Exchange:
    pass
