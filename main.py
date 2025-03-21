import os
import telegram
import logging

def vaupshasova_bot(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    #logging.warning("This is chat_id from Telegram. Bakunovich: ")
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        chat_id = update.message.chat.id
        text = update.message.text
        #bot.sendMessage(chat_id=chat_id, text=text + ": Vaupshasova Bot")

        if text == "/add@vaupshasova_bot":
            update.message.reply_text("Добавлен в состав на игру 22 марта под номером 1")

        if text == "/remove@vaupshasova_bot":
            update.message.reply_text("Удален из состава на игру 22 марта")

        if text == "/chair@vaupshasova_bot":
            update.message.reply_text("Сел на стульчик на игру 22 марта")
    return "Okie-Dockie"