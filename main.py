import os
import telebot
import command_add
import command_remove
import command_chair
import command_squad
import command_split
import command_talk
import command_wakeup
import command_register_lineups
import command_print_lineups
import command_season_stats
import command_alltime_stats
import command_balance
import command_how_much_we_owe
import command_my_balance
import command_my_stats
import command_register_game_stats
import command_register_money
import command_register_pitch_payment
import command_register_score
import command_score
import command_records
import alerts
import dotenv
from logger import log

dotenv.load_dotenv()
API_KEY = os.environ['TELEGRAM_API_TOKEN']
log("Environment variables loaded.")
bot = telebot.TeleBot(API_KEY)
log("Bot object initialized.")

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

@bot.message_handler(commands=['register_lineups'])
def register_lineups(message):
    command_register_lineups.execute(message, bot)

@bot.message_handler(commands=['print_lineups'])
def print_lineups(message):
    command_print_lineups.execute(message, bot)

@bot.message_handler(commands=['season_stats'])
def season_stats(message):
    command_season_stats.execute(message, bot)

@bot.message_handler(commands=['alltime_stats'])
def alltime_stats(message):
    command_alltime_stats.execute(message, bot)

@bot.message_handler(commands=['balance'])
def balance(message):
    command_balance.execute(message, bot)

@bot.message_handler(commands=['how_much_we_owe'])
def how_much_we_owe(message):
    command_how_much_we_owe.execute(message, bot)

@bot.message_handler(commands=['my_balance'])
def my_balance(message):
    command_my_balance.execute(message, bot)

@bot.message_handler(commands=['my_stats'])
def my_stats(message):
    command_my_stats.execute(message, bot)

@bot.message_handler(commands=['register_game_stats'])
def game_stats(message):
    command_register_game_stats.execute(message, bot)

@bot.message_handler(commands=['register_money'])
def register_money(message):
    command_register_money.execute(message, bot)

@bot.message_handler(commands=['register_pitch_payment'])
def register_pitch_payment(message):
    command_register_pitch_payment.execute(message, bot)

@bot.message_handler(commands=['register_score'])
def register_score(message):
    command_register_score.execute(message, bot)

@bot.message_handler(commands=['score'])
def score(message):
    command_score.execute(message, bot)

@bot.message_handler(commands=['records'])
def score(message):
    command_records.execute(message, bot)

alerts.schedule_alerts()
log("Alerts scheduled.")
log("Started polling.")
log("Bot is up and running.")
bot.infinity_polling()
