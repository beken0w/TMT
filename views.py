import os
from models import Task
from dotenv import load_dotenv

import telebot

load_dotenv()
bot = telebot.TeleBot(
    os.getenv("token",
              default="6233148573:AAFI1OqvrMkUVPgwfhBmyxTaqEfrYjC3vPo")
)


@bot.message_handler(commands=['start'])
def start_message(message):
    text = "Добро пожаловать\n"\
            "Список доступных команд:\n\n"\
            "/list - список задач,\n"\
            "/add - добавить задачу\n"\
            "/done <id> - завершить задачу\n"\
            "/delete <id> - удалить задачу\n"\
            "где <id> - уникальный номер задачи"

    bot.send_message(message.chat.id, text)


obj = Task()


@bot.message_handler(commands=['add'])
def get_task_info(message):
    bot.send_message(message.chat.id, "Введите заголовок задачи:")
    bot.register_next_step_handler(message, take_title)


def take_title(message):
    obj.add_value('title', message.text)
    bot.send_message(message.chat.id, "Введите описание задачи:")
    bot.register_next_step_handler(message, take_description)


def take_description(message):
    obj.add_value('description', message.text)
    bot.send_message(message.chat.id, "Задача создана!")
    bot.send_message(message.chat.id, obj.get_info())
    obj.insert_task()


@bot.message_handler(commands=['list'])
def get_task_list(message):
    bot.send_message(message.chat.id, obj.select_tasks(), parse_mode='HTML')


@bot.message_handler(commands=['done'])
def update_status(message):
    id = message.text.split(' ', 1)[1]
    text = "Статус задачи успешно обновлен"
    obj.update_status(id)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['delete'])
def delete_task(message):
    id = message.text.split(' ', 1)[1]
    text = "Задача успешно удалена"
    obj.delete_task(id)
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
