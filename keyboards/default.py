from telebot.types import ReplyKeyboardMarkup, KeyboardButton

cities2 = ["Toshkent", "Andijon", "Buxoro", "Guliston", "Jizzax", "Novoiy", "Namangan", "Nukus", "Samarqand",
           "Termiz", "Urganch", "Farg'ona", "Qarshi", "Marg'ilon", "Xiva", "Qo'qon", "Angren", "Bekobod",
           "Denov", "Zomin", "Zarafshon", "Nurota", "Pop", "Urgut", "Chust", "Shahrixon", "Qorako'l"]


def registr():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Ro'yxatdan o'tish uchun bosing!")
    markup.add(btn1)
    return markup


def phone_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Telefon raqam yuborish", request_contact=True)
    markup.add(btn1)
    return markup


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Tillarga qaytish")
    btn2 = KeyboardButton("Menu")
    markup.add(btn1, btn2)
    return markup


def tillar():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Detect language-English")
    btn2 = KeyboardButton("Detect language-Russia")
    btn3 = KeyboardButton("Detect language-Uzbek")
    btn4 = KeyboardButton("Detect language-Korean")
    btn5 = KeyboardButton("Detect language-Indonesia")
    btn6 = KeyboardButton("Detect language-Arabic")
    btnmenu = KeyboardButton("Menu")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btnmenu)
    return markup


def menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("Ro'za taqvimi")
    btn2 = KeyboardButton("Translate")
    btn3 = KeyboardButton("Instagram video downloader")
    btn4 = KeyboardButton("Ob havo")
    btn5 = KeyboardButton("qr-code")
    markup.add(btn1, btn2, btn3, btn4,btn5)
    return markup


def cities():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for i in cities2:
        btn = KeyboardButton(i)
        buttons.append(btn)
        if len(buttons) == 2:
            markup.add(*buttons)
            buttons.clear()
        
    markup.add(KeyboardButton("Menu"))
    return markup


def instagram_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Menu")
    markup.add(btn1)
    return markup


def ob_havo_menu():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = KeyboardButton("Shaharlar bo'yicha")
    btn2 = KeyboardButton("Joylashuv bo'yicha", request_location=True)
    btn3 = KeyboardButton("Menu")
    markup.add(btn1, btn2, btn3)
    return markup


def uz_citys():
    markup3 = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    city1 = KeyboardButton("Fergana")
    city2 = KeyboardButton("Namangan")
    city3 = KeyboardButton("Andijon")
    city4 = KeyboardButton("Toshkent")
    city5 = KeyboardButton("Navoiy")
    city6 = KeyboardButton("Jizzax")
    city7 = KeyboardButton("Samarqand")
    city8 = KeyboardButton("Xorazm")
    city9 = KeyboardButton("Buxoro")
    city10 = KeyboardButton("Qashqadaryo")
    city11 = KeyboardButton("Sirdaryo")
    city12 = KeyboardButton("Surxandaryo")
    button3 = KeyboardButton("Menu")
    markup3.add(city1, city11, city12, city10, city5, city6, city7, city8, city9, city2, city3, city4, button3)
    return markup3
