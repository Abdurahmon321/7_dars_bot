import os.path

from data.loader import bot, db
from telebot.types import Message, ReplyKeyboardRemove
from keyboards.default import phone_button, tillar, main_menu, cities, menu, registr
from googletrans import Translator
translater = Translator()
USER_DATA = {}

cities2 = ["Toshkent", "Andijon", "Buxoro", "Guliston", "Jizzax", "Navoiy", "Namangan", "Nukus", "Samarqand",
           "Termiz", "Urganch", "Farg'ona", "Qarshi", "Marg'ilon", "Xiva", "Qo'qon", "Angren", "Bekobod",
           "Denov", "Zomin", "Zarafshon", "Nurota", "Pop", "Urgut", "Chust", "Shaxrihon", "Qorako'l"]


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
        bot.send_message(chat_id, "NImadur hato bo'ldi boshidan royxatdan o'ting", reply_markup=registr())
        bot.register_next_step_handler(message, registration)


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
        bot.send_message(chat_id, "NImadur hato bo'ldi", reply_markup=phone_button())
        bot.register_next_step_handler(message, get_phone)


@bot.message_handler(func=lambda message: message.text == "Translate")
def translate(message: Message):
    bot.send_message(message.chat.id, "Tilni tanlang", reply_markup=tillar())

LANG = {}


@bot.message_handler(func=lambda message: str(message.text).startswith("Detect language") and "-" in message.text)
def tranlate_uz_ru(message: Message):
    lan = message.text.split("-")
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    LANG[from_user_id] = {}
    print(LANG)
    LANG[from_user_id]["to_lang"] = str(lan[1][:2])
    msg = bot.send_message(chat_id, "Text kiriting: ")
    bot.register_next_step_handler(msg, tralate_text)

# @bot.message_handler(content_types=["text"])
def tralate_text(message: Message,):
    chat_id = message.chat.id
    text = message.text

    if message.text == "Menu":
        print('Menu')
    elif message.text == 'Tillarga qaytish':
        print('Tillarga qaytish')
    else:
        from_user_id = message.from_user.id
        lang = LANG[from_user_id]['to_lang']

        tr_text = translater.translate(text, dest=LANG[from_user_id4]["to_lang"].lower()).text
        msg = bot.send_message(chat_id, f"{'en'} \n{text}\n\n {str(LANG[from_user_id]["to_lang"])}\n {tr_text}", reply_markup=main_menu())
        bot.register_next_step_handler(msg, tralate_text)


@bot.message_handler(func=lambda message: message.text == "Tillarga qaytish")
def tillarga_qaytish(message: Message):
    bot.send_message(message.chat.id, "Tilni tanlang: ", reply_markup=tillar())
    bot.register_next_step_handler(message, tranlate_uz_ru)


@bot.message_handler(func=lambda message: message.text == "Menu")
def menu2(message: Message):
    bot.send_message(message.chat.id, "Bosh menuga qaytildi", reply_markup=menu())


@bot.message_handler(func=lambda message: message.text == "Ro'za taqvimi")
def taqvim(message: Message):
    if message.text == "Menu":
        bot.send_message(message.chat.id, "Bosh menuga qaytildi", reply_markup=menu())
    bot.send_message(message.chat.id, "Shaxarni tanlang", reply_markup=cities())


@bot.message_handler(func=lambda message: message.text in cities2)
def send_photo(message: Message):
    chat_id = message.chat.id
    city_name = message.text
    file_path = os.path.join("shaharlar", f"{city_name.lower()}.png")
    photo = open(file_path, mode="rb")
    bot.send_photo(chat_id, photo, caption=f"{city_name} shaxrining ro'za taqvimi")
