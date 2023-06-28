from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def permanent_kb():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("💬 Команды")
    btn2 = KeyboardButton("📜 Список задач")
    btn3 = KeyboardButton("📝 Добавить задачу")
    btn4 = KeyboardButton("💱 Курс 'МИР'")
    btn5 = KeyboardButton("Конвертировать рубли в валюту")
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    return keyboard

