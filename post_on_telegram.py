import json
import os
from telegram import Bot, InputMediaPhoto

def post_on_telegram(posts="", date=""):
    with open("telegram_cred.json", "r") as file:
        data = json.load(file)
        token = data["ACCESS_TOKEN"]
        chat_id = data["CHAT_ID"]

    if posts == "":
        with open(f"post/telegram/{date}.txt", "r", encoding="utf-8") as file:
            posts = file.read()
    bot = Bot(token)
    print("Sending message to telegram...")
    bot.send_message(chat_id=chat_id, text=posts, parse_mode="HTML")
    print("Message sent successfully.")

    medium = []
    for img in os.listdir(f"img/{date}"):
        media = InputMediaPhoto(open(f"img/{date}/{img}", "rb"))
        medium.append(media)
        
    print("Sending photos to telegram...")
    if len(medium) >= 2:
        bot.send_media_group(chat_id=chat_id, media=medium, timeout=1000)
    else:
        bot.send_photo(chat_id=chat_id, photo=open(f"img/{date}/1.png", "rb"), timeout=1000)
    print("All Done!")

