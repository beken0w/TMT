import os
import logging
import datetime

import telebot
from telebot import types
from dotenv import load_dotenv

from models import Task, Exchange
from core.keyboards.reply import permanent_kb
from core.keyboards.inline import delete_kb, done_delete_kb, currency_kb
from parse_exchange import convert_to_rub, count_rub, parse_mir


logging.basicConfig(level=logging.INFO,
                    filename='log_file.log',
                    filemode='a')

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
money = Exchange()


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
    bot.send_message(message.chat.id, text=text, reply_markup=permanent_kb())
    logging.info("Приветствие пользователя")


def get_task_info(message):
    bot.send_message(message.chat.id, "🔤 Введите заголовок задачи:")
    bot.register_next_step_handler(message, take_title)


def take_title(message):
    obj.add_value('title', message.text)
    bot.send_message(message.chat.id, "🔤 Введите описание задачи:")
    bot.register_next_step_handler(message, take_description)


def take_description(message):
    obj.add_value('description', message.text)
    obj.insert_task(message.from_user.id)
    bot.send_message(message.chat.id, "❕ Задача создана!")
    chat_id = message.chat.id
    ids, statuses, result = obj.get_created_task()
    if statuses[0] == 0:
        keyboard = done_delete_kb(ids[0])
    else:
        keyboard = delete_kb(ids[0])
    bot.send_message(chat_id=chat_id, text=result[0], reply_markup=keyboard)
    logging.info("Задача создана")


def update_status(message):
    id = message.data.split()[1]
    chat_id = message.message.chat.id

    if obj.is_exist(id) == (1,) and obj.check_status(id) != (1,):
        obj.update_status(id)
        return True
    elif obj.check_status(id) == (1,):
        text = "❗ Задача ранее была отмечена выполненной"
        logging.error("Попытка выполнить уже завершенную задачу")
    else:
        text = "❗ Задачи с данным id не существует"
    bot.send_message(chat_id=chat_id, text=text)
    logging.info(f"Отработала функция UPDATE_STATUS: {text}")
    return False


def delete_task(message):
    id = message.data.split()[1]
    chat_id = message.message.chat.id
    logging.info("Работает функция DELETE_TASK")
    if obj.is_exist(id) == (1,):
        obj.delete_task(id)
        return True
    else:
        text = "❗ Задачи с данным id не существует"
        bot.send_message(chat_id=chat_id, text=text)
        return False


def get_task_list(message):
    chat_id = message.chat.id
    ids, statuses, result = obj.select_tasks(message.from_user.id)
    if len(ids) > 0:
        for i in range(len(ids)):
            if statuses[0] == 0:
                keyboard = done_delete_kb(ids[0])
            else:
                keyboard = delete_kb(ids[0])
            bot.send_message(chat_id=chat_id, text=result[i],
                             reply_markup=keyboard)
        logging.info("Отработала функция GET_TASK_LIST")
    else:
        bot.send_message(chat_id=chat_id, text="❕ Список задач пуст")
        logging.info("Отработала функция GET_TASK_LIST: Список задач пуст")


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data in parse_mir():
        convert_currency(call)
        return
    chat_id = call.message.chat.id
    arg = call.data.split()[1]
    if arg.isdigit():
        if call.data.startswith('/delete'):
            logging.info("Команда /delete запущена с кнопки")
            if delete_task(call):
                text = call.message.text.replace('💼', '').replace('✅', '')[:call.message.text.find('\n')]
                new_message_text = f"{text} успешно удалена"
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text=new_message_text)

        elif call.data.startswith('/done'):
            logging.info("Команда /done запущена с кнопки")
            if update_status(call):
                keyboard = delete_kb(call.data.split()[1])
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
    elif message.text == "💱 Курс 'МИР'":
        bot.send_message(message.chat.id, text=convert_to_rub())
    elif message.text == "Конвертировать рубли в валюту":
        count_curr_1(message)
    else:
        bot.send_message(message.chat.id, text="❗ Такой команды не существует")
        actual_commands(message)


def count_curr_1(message):
    bot.send_message(message.chat.id, "🔤 Введите сумму в рублях:")
    bot.register_next_step_handler(message, count_curr_2)


def count_curr_2(message):
    if message.text.strip().isdigit():
        money.__setattr__('value', float(message.text.replace(",", ".")))
        keyboard = currency_kb(parse_mir())
        bot.send_message(chat_id=message.chat.id, text="Выберите валюту в которую конвертируете:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "🔤 Введите корректную сумму в рублях:")
        bot.register_next_step_handler(message, count_curr_2)


def convert_currency(call):
    curr = parse_mir()[call.data]
    res = money.value * curr
    bot.send_message(call.message.chat.id, res)


if __name__ == '__main__':
    bot.polling(none_stop=True)

# 1 рубль == 4.433 - Армянский драм
# 1 рубль == 28.811 - Белорусский рубль
# 1 рубль == 3.063 - Венесуэльский боливар
# 1 рубль == 272.777 - Вьетнамский донг
# 1 рубль == 5.156 - Казахстанский тенге
# 1 рубль == 1.361 - Кубинский песо
# 1 рубль == 1.006 - Кыргызский сом
# 1 рубль == 7.791 - Таджикский сомони
# 1 рубль == 131.7 - Узбекский сум