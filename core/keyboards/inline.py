from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def delete_kb(id):
    keyboard = InlineKeyboardMarkup()
    delete_button = InlineKeyboardButton(
        text="🗑️ Удалить задачу", callback_data=f'/delete {id}')
    keyboard.add(delete_button)
    return keyboard


def done_delete_kb(id):
    keyboard = InlineKeyboardMarkup()
    delete_button = InlineKeyboardButton(
        text="🗑️ Удалить задачу", callback_data=f'/delete {id}')
    status_button = InlineKeyboardButton(
            text="✔️ Выполнить задачу", callback_data=f'/done {id}')
    keyboard.add(status_button, delete_button)
    return keyboard


def currency_kb(curr):
    keyboard = InlineKeyboardMarkup()
    btns = [InlineKeyboardButton(text=key, callback_data=key) for key in curr]
    keyboard.add(*btns)
    return keyboard
