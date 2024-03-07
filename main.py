from data.loader import db, bot
import handlers
db.create_table_users()
text = "Detect language-RU"
print(len(text))

if __name__ == "__main__":
    bot.infinity_polling()
