import sqlite3


class Task:

    def add_value(self, name, value):
        setattr(self, name, value)

    def get_info(self):
        return f"Заголовок: {self.title}\nОписание: {self.description}"

    def beautify_response(self, rows):
        result = []
        for row in rows:
            result.append("=======================================")
            result.append(f"id: {row[0]}\n"
                          f"Заголовок: {row[1]}\n"
                          f"Описание: {row[2]}\n"
                          f"Статус: {'Выполняется' if row[3] == 0 else 'Завершена'}\n")
            if row[3] == 0:
                result.append(f"Завершить задачу: <a href='tg://bot_command?/done {row[0]}'>/done {row[0]}</a>\n"
                              f"Удалить задачу <a href='tg://bot_command?/delete {row[0]}'>/delete {row[0]}</a>")
            else:
                result.append(f'Удалить задачу /delete {row[0]}')
        result.append("=======================================")
        return "\n".join(result)

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
        cursor.execute('update tasks set status = 1 where id = ?;', (id))
        conn.commit()
        conn.close()
        print("Connection disconnected!")

    def delete_task(self, id):
        conn = sqlite3.connect('main.db')
        cursor = conn.cursor()
        print("Connection successful!")
        cursor.execute('delete from tasks where id = ?;', (id))
        conn.commit()
        conn.close()
        print("Connection disconnected!")
