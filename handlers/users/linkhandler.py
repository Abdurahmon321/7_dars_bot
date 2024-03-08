from data.loader import bot
from telebot.types import Message
from keyboards.default import menu
from pytube import YouTube
import os

@bot.message_handler(func=lambda message: str(message.text).startswith("https://www.instagram"))
def intagram_link(message: Message):
    link = str(message.text).replace("www.", "dd")
    bot.send_message(message.chat.id, link, reply_markup=menu())


# @bot.message_handler(func=lambda message: "https://youtube" in message.text)
# def youtube_link(message: Message):
#     yt = YouTube(message.text)
#     video = yt.streams.get_highest_resolution()
#     video.download("video")
#     bot.send_video(message.chat.id, video)
#
