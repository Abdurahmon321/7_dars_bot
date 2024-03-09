import os

import requests

from data.loader import bot
from telebot.types import Message
from keyboards.default import instagram_menu
from handlers.users.text_handlers import menu2
import qrcode


@bot.message_handler(func=lambda message: message.text == "qr-code")
def qr_code(message: Message):
    bot.send_message(message.chat.id, "qr code qilish uchun text, link, photo jo'nating", reply_markup=instagram_menu())
    bot.register_next_step_handler(message, generate_qr_code)


def generate_qr_code(message: Message):
    if message.text == "Menu":
        menu2(message)
    else:
        if message.text:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(message.text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("qr_code.png")  # Save QR code image to a file
            with open("qr_code.png", "rb") as photo:
                bot.send_photo(message.chat.id, photo, reply_markup=instagram_menu())
            os.remove("qr_code.png")
            bot.register_next_step_handler(message, generate_qr_code)
        elif message.photo:
            photo_id = message.photo[-1].file_id
            file_info = bot.get_file(photo_id)
            file_path = file_info.file_path
            file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"

            response = requests.get(file_url)
            with open("photo.jpg", "wb") as photo_file:
                photo_file.write(response.content)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(file_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("qr_code.png")
            with open("qr_code.png", "rb") as qr_photo:
                bot.send_photo(message.chat.id, qr_photo, reply_markup=instagram_menu())
            os.remove("qr_code.png")
            os.remove("photo.jpg")
            bot.register_next_step_handler(message, generate_qr_code)
        else:
            bot.send_message(message.chat.id, "Hatolik mavjud qaytadan urinib ko'ring")
            bot.register_next_step_handler(message, generate_qr_code)
