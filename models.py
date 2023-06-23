import sqlite3


class Task:

    def add_value(self, name, value):
        setattr(self, name, value)

    def get_info(self):
        return f"Заголовок: {self.title}\nОписание: {self.description}"

    def beautify_response(self, rows):
        statuses = []
        ids = []
        result = []
        for row in rows:
            ids.append(row[0])
            statuses.append(row[3])
            result.append(f"{' '*40}Задача №{row[0]}\n\n"
                          f"Заголовок: {row[1]}\n"
                          f"Описание: {row[2]}\n"
                          f"Статус: {'💼 Невыполнена' if row[3] == 0 else '✅ Выполнена'}")
        return ids, statuses, result

    def select_tasks(self):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        print("Connection successful!")
        cursor.execute('SELECT * from tasks')
        text = self.beautify_response(cursor.fetchall())
        conn.commit()
        conn.close()
        print("Connection disconnected!")
        return text

    def insert_task(self):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        print("Connection successful!")
        cursor.execute('INSERT INTO tasks (title, description) VALUES(?, ?);',
                       (self.title, self.description))
        conn.commit()
        conn.close()
        print("Connection disconnected!")

    def update_status(self, id):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        print("Connection successful!")
        cursor.execute('update tasks set status = 1 where id = ?;', (id,))
        conn.commit()
        conn.close()
        print("Connection disconnected!")

    def delete_task(self, id):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        print("Connection successful!")
        cursor.execute('delete from tasks where id = ?;', (id,))
        conn.commit()
        conn.close()
        print("Connection disconnected!")
