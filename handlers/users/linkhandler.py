from data.loader import bot
from telebot.types import Message
from keyboards.default import instagram_menu
from handlers.users.text_handlers import menu2


@bot.message_handler(func=lambda message: message.text == "Instagram video downloader")
def intagram_link(message: Message):
    bot.send_message(message.chat.id, "Instagram link jo'nating", reply_markup=instagram_menu())
    bot.register_next_step_handler(message, instagram_downloader)


def instagram_downloader(message: Message):
    if message.text == "Menu":
        menu2(message)
    else:
        try:
            link = str(message.text).replace("www.", "dd")
            bot.send_video(message.chat.id, link, reply_markup=instagram_menu())
            bot.register_next_step_handler(message, instagram_downloader)
        except:
            bot.send_message(message.chat.id, "Videoni yuklab bo'lmadi qayta urinib ko'ring")
            bot.register_next_step_handler(message, instagram_downloader)
