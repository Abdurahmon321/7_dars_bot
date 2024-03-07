from data.loader import bot, db
from telebot.types import Message


@bot.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    db.insert_tg_id(from_user_id)

    bot.send_message(chat_id, "Translate botiga xush kelibsz!")


