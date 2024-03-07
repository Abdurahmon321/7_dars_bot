from data.loader import bot, db
from telebot.types import Message, ReplyKeyboardRemove
from keyboards.default import phone_button
USER_DATA = {}


@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish uchun bosing!")
def registration(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    msg = bot.send_message(chat_id, "Ism va Familyangizni kiriting")
    USER_DATA[from_user_id] = {}
    bot.register_next_step_handler(msg, get_name)


def get_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    full_name = message.text
    name = full_name.split()
    if len(name) == 2 and name[0].isalpha() and name[1].isalpha():
        USER_DATA[from_user_id]["full_name"] = full_name
        msg = bot.send_message(chat_id, "Telefon raqamini yuborish buttonini bosing", reply_markup=phone_button())
        bot.register_next_step_handler(msg, get_phone)
    else:
        registration()


def get_phone(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    full_name = USER_DATA[from_user_id]['full_name']

    if message.contact:
        phone_number = message.contact.phone_number
    else:
        phone_number = message.text

    if len(phone_number) == 13 and phone_number[1::].isdigit():
        USER_DATA[from_user_id]["phone_number"] = phone_number
        db.update_from_telegram_id(telegram_id=from_user_id, full_name=full_name, phone_number=phone_number)
        bot.send_message(chat_id, "Ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardRemove())
    else:
        registration()
