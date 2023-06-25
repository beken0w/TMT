import os
import logging
import datetime

import telebot
from telebot import types
from dotenv import load_dotenv

from models import Task


logging.basicConfig(level=logging.INFO,
                    filename='log_file.log',
                    filemode='a',
                    encoding='UTF-8')

load_dotenv()
if os.getenv("token") is not None:
    try:
        bot = telebot.TeleBot(os.getenv("token"))
        date_time = datetime.datetime.now().replace(microsecond=0)
        logging.info(f"\n{'='*30}[ {date_time} ]{'='*30}\n")
        logging.info("Токен успешно получен. Запускаю бота")
    except Exception as e:
        logging.critical(f"Возникла проблема c активацией бота:\n{e}")
        raise Exception(f"Возникла проблема c активацией бота:\n{e}")
else:
    logging.critical("Отсутствует токен бота в переменных окружения")
    raise Exception("Отсутствует токен бота в переменных окружения")

obj = Task()


@bot.message_handler(commands=['commands'])
def actual_commands(message):
    text =  "Список доступных команд:\n\n"\
            "/list - список задач,\n"\
            "/add - добавить задачу\n"\
            "/done <id> - завершить задачу\n"\
            "/delete <id> - удалить задачу\n"\
            "где <id> - уникальный номер задачи"
    bot.send_message(message.chat.id, text=text)
    logging.info("Отправил в чат доступные команды")


@bot.message_handler(commands=['start'])
def start_message(message):
    text = "Добро пожаловать в TO-DO List\n\n"\
            "    Возможности бота:\n\n"\
            "📝  добавлять задачи\n\n"\
            "✔️  изменять статус задачи\n\n"\
            "🗑️  удалять задачи"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💬 Команды")
    btn2 = types.KeyboardButton("📜 Список задач")
    btn3 = types.KeyboardButton("📝 Добавить задачу")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text=text, reply_markup=markup)
    logging.info("Приветствие пользователя")


@bot.message_handler(commands=['add'])
def get_task_info(message):
    bot.send_message(message.chat.id, "🔤 Введите заголовок задачи:")
    bot.register_next_step_handler(message, take_title)


def take_title(message):
    obj.add_value('title', message.text)
    bot.send_message(message.chat.id, "🔤 Введите описание задачи:")
    bot.register_next_step_handler(message, take_description)


def take_description(message):
    obj.add_value('description', message.text)
    obj.insert_task()
    bot.send_message(message.chat.id, "❕ Задача создана!")
    chat_id = message.chat.id
    ids, statuses, result = obj.get_created_task()
    keyboard = types.InlineKeyboardMarkup()
    delete_button = types.InlineKeyboardButton(
        text="🗑️ Удалить задачу", callback_data=f'/delete {ids[0]}')
    if statuses[0] == 0:
        status_button = types.InlineKeyboardButton(
            text="✔️ Выполнить задачу", callback_data=f'/done {ids[0]}')
        keyboard.add(status_button, delete_button)
    else:
        keyboard.add(delete_button)
    bot.send_message(chat_id=chat_id, text=result[0], reply_markup=keyboard)
    logging.info("Задача создана")


@bot.message_handler(commands=['done'])
def update_status(message, from_button=False):
    if not from_button:
        if len(message.text) < 7:
            bot.send_message(message.chat.id, text="❗ Не хватает ID задачи")
            logging.error("Не хватает ID задачи")
            return
        else:
            id = message.text.split()[1]
            chat_id = message.chat.id
    else:
        id = message.data.split()[1]
        chat_id = message.message.chat.id

    if id.isdigit() and obj.is_exist(id) == (1,):
        if obj.check_status(id) != (1,):
            obj.update_status(id)
            text = "❕ Задача отмечена выполненной"
        else:
            text = "❗ Задача ранее была отмечена выполненной"
            logging.error("Попытка выполнить уже завершенную задачу")
    else:
        text = "❗ Задачи с данным id не существует"
    bot.send_message(chat_id=chat_id, text=text)
    logging.info(f"Отработала функция UPDATE_STATUS: {text}")


@bot.message_handler(commands=['delete'])
def delete_task(message, from_button=False):
    if not from_button:
        if len(message.text) < 9:
            bot.send_message(message.chat.id, text="❗ Не хватает ID задачи")
            logging.error("❗ Не хватает ID задачи")
            return
        else:
            id = message.text.split()[1]
            chat_id = message.chat.id
    else:
        id = message.data.split()[1]
        chat_id = message.message.chat.id

    if obj.is_exist(id) == (1,):
        obj.delete_task(id)
        text = "❕ Задача успешно удалена"
    else:
        text = "❗ Задачи с данным id не существует"
    bot.send_message(chat_id=chat_id, text=text)
    logging.info(f"Отработала функция DELETE_TASK: {text}")


@bot.message_handler(commands=['list'])
def get_task_list(message):
    chat_id = message.chat.id
    ids, statuses, result = obj.select_tasks()
    if len(ids) > 0:
        for i in range(len(ids)):
            keyboard = types.InlineKeyboardMarkup()
            delete_button = types.InlineKeyboardButton(
                text="🗑️ Удалить задачу",
                callback_data=f'/delete {ids[i]}')
            if statuses[i] == 0:
                status_button = types.InlineKeyboardButton(
                    text="✔️ Выполнить задачу",
                    callback_data=f'/done {ids[i]}')
                keyboard.add(status_button, delete_button)
            else:
                keyboard.add(delete_button)
            bot.send_message(chat_id=chat_id, text=result[i],
                             reply_markup=keyboard)
        logging.info("Отработала функция GET_TASK_LIST")
    else:
        bot.send_message(chat_id=chat_id, text="❕ Список задач пуст")
        logging.info("Отработала функция GET_TASK_LIST: Список задач пуст")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    arg = call.data.split()[1]
    if arg.isdigit():
        if call.data.startswith('/delete'):
            logging.info("Команда /delete запущена с кнопки")
            bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
            delete_task(call, True)

        elif call.data.startswith('/done'):
            logging.info("Команда /done запущена с кнопки")
            update_status(call, True)
            keyboard = types.InlineKeyboardMarkup()
            button2 = types.InlineKeyboardButton(text='Удалить задачу',
                                                 callback_data=f"/delete {call.data.split()[1]}")
            keyboard.add(button2)
            new_message_text = call.message.text.replace('💼 Не выполнена', '✅ Выполнена')
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=new_message_text)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=keyboard)

    else:
        bot.send_message(chat_id, text="❗ Не хватает ID задачи")
        logging.error("Не хватает ID задачи")


@bot.message_handler(content_types=['text'])
def urls(message):
    if message.text == "💬 Команды":
        actual_commands(message)
    elif message.text == "📜 Список задач":
        get_task_list(message)
    elif message.text == "📝 Добавить задачу":
        get_task_info(message)
    else:
        bot.send_message(message.chat.id, text="❗ Такой команды не существует")
        actual_commands(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
