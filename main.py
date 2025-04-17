import os
import telebot
import command_add
import command_remove
import command_chair
import command_squad
import command_split
import command_talk
import command_wakeup
import alerts
import dotenv
from logger import log

dotenv.load_dotenv()
API_KEY = os.environ['TELEGRAM_API_TOKEN']
log("Environment variables loaded.")
bot = telebot.TeleBot(API_KEY)
#bot.remove_webhook()
#bot.set_webhook("https://europe-central2-angular-lambda-289018.cloudfunctions.net/vaupshasova_bot")
log("Bot object initialized.")


def vaupshasova_bot(request):
    if request.method == "POST":
        bot = telebot.TeleBot(API_KEY)
        request_body_dict = request.get_json(force=True)
        update = telebot.types.Update.de_json(request_body_dict)
        bot.register_message_handler(callback=add, commands=['add'])
        bot.register_message_handler(callback=remove, commands=['remove'])
        bot.register_message_handler(callback=chair, commands=['chair'])
        bot.register_message_handler(callback=squad, commands=['squad'])
        bot.register_message_handler(callback=split, commands=['split'])
        bot.register_message_handler(callback=talk, commands=['talk'])
        bot.register_message_handler(callback=wakeup, commands=['wakeup'])
        bot.process_new_updates([update])
        log("Webhook Invoked: " + update.message.text)
    return "OK"


@bot.message_handler(commands=['add'])
def add(message):
    command_add.execute(message, bot)


@bot.message_handler(commands=['remove'])
def remove(message):
    command_remove.execute(message, bot)


@bot.message_handler(commands=['chair'])
def chair(message):
    command_chair.execute(message, bot)


@bot.message_handler(commands=['squad'])
def squad(message):
    command_squad.execute(message, bot)


@bot.message_handler(commands=['split'])
def split(message):
    command_split.execute(message, bot)


@bot.message_handler(commands=['talk'])
def talk(message):
    command_talk.execute(message, bot)


@bot.message_handler(commands=['wakeup'])
def wakeup(message):
    command_wakeup.execute(message, bot)

alerts.schedule_alerts()
log("Alerts scheduled.")

#log("Webhook URL: " + bot.get_webhook_info().url)
log("Started polling.")
log("Bot is up and running.")
bot.infinity_polling()
