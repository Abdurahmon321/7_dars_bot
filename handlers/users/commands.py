from data.loader import bot, db
from telebot.types import Message, ReplyKeyboardRemove
from keyboards.default import registr


@bot.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    db.insert_tg_id(tg_id=from_user_id)

    check = db.check_user(tg_id=from_user_id)
    print(check)
    bot.send_message(chat_id, "ishladi")
    if None in check:
        text = "Ro'yxatdan o'tish tugmasini bosing"
        markup = registr()
        # bot.send_message(chat_id, "Ro'yxatdan o'tish tugamasini bosing!", reply_markup=registr())
    else:
        text = "siz ro'yxatdan o'tib bo'lgansz"
        markup = ReplyKeyboardRemove()
        # bot.send_message(chat_id, "Siz ro'yxatdan o'tib bo'lgansz", reply_markup=ReplyKeyboardRemove())

    bot.send_message(chat_id, text, reply_markup=markup)