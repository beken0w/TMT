import os
from models import Task
from dotenv import load_dotenv

import telebot
from telebot import types


load_dotenv()
bot = telebot.TeleBot(
    os.getenv("token",
              default="6233148573:AAFI1OqvrMkUVPgwfhBmyxTaqEfrYjC3vPo")
)


@bot.message_handler(commands=['commands'])
def actual_commands(message):
    text =  "Список доступных команд:\n\n"\
            "/list - список задач,\n"\
            "/add - добавить задачу\n"\
            "/done <id> - завершить задачу\n"\
            "/delete <id> - удалить задачу\n"\
            "где <id> - уникальный номер задачи"
    bot.send_message(message.chat.id, text=text)


@bot.message_handler(commands=['start'])
def start_message(message):
    text = "Добро пожаловать\n"\
            "Вы открыли TO-DO List\n"\
            "Вы можете добавлять задачи\n"\
            "Изменять их статус\n"\
            "Удалять из базы"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Доступные команды")
    btn2 = types.KeyboardButton("Список задач")
    btn3 = types.KeyboardButton("Добавить задачу")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Доступные команды":
        actual_commands(message)
    elif message.text == "Список задач":
        get_task_list(message)
    elif message.text == "Добавить задачу":
        get_task_info(message)
    elif message.text.startswith("/done"):
        update_status(message)
    elif message.text.startswith("/delete"):
        delete_task(message)

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


@bot.message_handler(commands=['done'])
def update_status(message, id=None, chat_id=None):
    if id is None:
        id = message.text.split(' ', 1)[1]
    if chat_id is None:
        chat_id = message.chat.id
    text = "Задача отмечена выполненной"
    print(id, message.text, sep='==')
    obj.update_status(id)
    bot.send_message(chat_id=chat_id, text=text)


@bot.message_handler(commands=['delete'])
def delete_task(message, id=None, chat_id=None):
    if id is None:
        id = message.text.split(' ', 1)[1]
    if chat_id is None:
        chat_id = message.chat.id
    text = "Задача успешно удалена"
    obj.delete_task(id)
    bot.send_message(chat_id=chat_id, text=text)


@bot.message_handler(commands=['list'])
def get_task_list(message):
    chat_id = message.chat.id
    ids, statuses, result = obj.select_tasks()
    if len(ids) > 0:
        for i in range(len(ids)):
            keyboard = types.InlineKeyboardMarkup()
            delete_button = types.InlineKeyboardButton(text=f"🗑️ Удалить задачу", callback_data=f'/delete {ids[i]}')
            if statuses[i] == 0:
                status_button = types.InlineKeyboardButton(text=f"✅ Выполнить задачу", callback_data=f'/done {ids[i]}')
                keyboard.add(status_button, delete_button)
            else:
                keyboard.add(delete_button)
            bot.send_message(chat_id=chat_id, text=result[i], reply_markup=keyboard)
    else:
        bot.send_message(chat_id=chat_id, text="Вы еще не добавили задачи")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    arg = call.data.split()[1]
    if call.data.startswith('/delete'):
        delete_task(call.data, id=arg, chat_id=chat_id)
    elif call.data.startswith('/done'):
        update_status(call.data, id=arg, chat_id=chat_id)


bot.polling(none_stop=True)
