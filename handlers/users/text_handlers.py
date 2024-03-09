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
        phone_number = "+" + phone_number
        print("1-if ishladi")
    else:
        phone_number = message.text
        print("1-else ishladi")

    if len(phone_number) == 13 and phone_number[1::].isdigit():
        print("ishlaadi")
        USER_DATA[from_user_id]["phone_number"] = phone_number
        db.update_from_telegram_id(telegram_id=from_user_id, full_name=full_name, phone_number=phone_number)
        bot.send_message(chat_id, "Ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, "Nimadur hato bo'ldi", reply_markup=phone_button())
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
    LANG[from_user_id]["from_lang"] = str(lan[0])
    LANG[from_user_id]["to_lang"] = str(lan[1][:2])
    msg = bot.send_message(chat_id, "Text kiriting: ")
    bot.register_next_step_handler(msg, tralate_text)

# @bot.message_handler(content_types=["text"])
def tralate_text(message: Message,):
    chat_id = message.chat.id
    text = message.text

    if message.text == "Menu":
        menu2(message)
    elif message.text == 'Tillarga qaytish':
        tillarga_qaytish(message)
    else:
        from_user_id = message.from_user.id
        lang = LANG[from_user_id]['to_lang']

        tr_text = translater.translate(text, dest=LANG[from_user_id]["to_lang"].lower()).text
        msg = bot.send_message(chat_id, f"{LANG[from_user_id]["from_lang"]} \n{text}\n\n {str(LANG[from_user_id]["to_lang"])}\n {tr_text}", reply_markup=main_menu())
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
    bot.send_message(message.chat.id, "Shaxarni tanlang", reply_markup=cities())
    bot.register_next_step_handler(message, send_photo)


def send_photo(message: Message):
    text1 = "نَوَيْتُ أَنْ أَصُومَ صَوْمَ شَهْرَ رَمَضَانَ مِنَ الْفَجْرِ إِلَى الْمَغْرِبِ، خَالِصًا لِلهِ تَعَالَى أَللهُ أَكْبَرُ"
    text2 = "اَللَّهُمَّ لَكَ صُمْتُ وَ بِكَ آمَنْتُ وَ عَلَيْكَ تَوَكَّلْتُ وَ عَلَى رِزْقِكَ أَفْتَرْتُ، فَغْفِرْلِى مَا قَدَّمْتُ وَ مَا أَخَّرْتُ بِرَحْمَتِكَ يَا أَرْحَمَ الرَّاحِمِينَ"
    full_text = (f"*Ro‘za tutish (saharlik, og‘iz yopish) duosi*\n\n{text1}\n\n"
                 f"Navaytu an asuvma sovma shahri ramazona minal fajri ilal mag‘ribi, xolisan lillahi ta’aalaa"
                 f" Allohu akbar.\n\n"
                 f"Ma’nosi: Ramazon oyining ro‘zasini subhdan to kun botguncha tutmoqni niyat qildim. "
                 f"Xolis Alloh uchun Alloh buyukdir.\n\n"
                 f"*Iftorlik (og‘iz ochish) duosi*\n\n{text2}\n\n"
                 f"Allohumma laka sumtu va bika aamantu va a’layka tavakkaltu va a’laa rizqika aftartu, "
                 f"fag‘firliy ma qoddamtu va maa axxortu birohmatika yaa arhamar roohimiyn.\n\n"
                 f"Ma’nosi: Ey Alloh, ushbu Ro‘zamni Sen uchun tutdim va Senga iymon keltirdim va Senga tavakkal "
                 f"qildim va bergan rizqing bilan iftor qildim. Ey mehribonlarning eng mehriboni, mening avvalgi va "
                 f"keyingi gunohlarimni mag‘firat qilgil.\n\n"
                 f"Manba: Muslim.uz")
    if message.text == "Menu":
        menu2(message)
    else:
        chat_id = message.chat.id
        city_name = message.text
        file_path = os.path.join("shaharlar", f"{city_name.lower()}.png")
        photo = open(file_path, mode="rb")
        bot.send_photo(chat_id, photo, caption=f"{city_name} shaxrining ro'za taqvimi", parse_mode="Markdown")
        bot.send_message(chat_id, full_text, parse_mode="Markdown")
        bot.register_next_step_handler(message, send_photo)
