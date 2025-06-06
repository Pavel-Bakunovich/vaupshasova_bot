from apscheduler.schedulers.background import BackgroundScheduler
import os
import telebot
import deepseek
import constants
from logger import log, log_error
from pytz import timezone
from helpers import get_next_matchday_formatted, get_today_minsk_time_formatted, fill_template,format_date
import database
from backup import Database_backup
from weather import Weather

API_KEY = os.environ['TELEGRAM_API_TOKEN']
bot = telebot.TeleBot(API_KEY)
scheduler = None

def schedule_alerts():
    scheduler = BackgroundScheduler()
    scheduler.add_job(start_registration,
                      'cron',
                      day_of_week='mon',
                      hour=8,
                      minute=0,
                      timezone=timezone('Europe/Minsk'))
    scheduler.add_job(start_waking_up, 
                      'cron',
                      day_of_week='sat',
                      hour=6,
                      minute=0,
                      timezone=timezone('Europe/Minsk'))
    scheduler.add_job(good_morning,
                      'cron',
                      hour=7,
                      minute=0,
                      timezone=timezone('Europe/Minsk'))

    scheduler.add_job(pitch_payment_reminder, 
                      'cron',
                      day_of_week='fri',
                      hour=15,
                      minute=0,
                      timezone=timezone('Europe/Minsk'))
    
    scheduler.add_job(daily_backup,
                      'cron',
                      hour=5,
                      minute=0,
                      timezone=timezone('Europe/Minsk'))

    scheduler.start()


def start_registration():
    try:
        bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, fill_template("📝 Погнали регистрироваться на {date}! /add", date=get_next_matchday_formatted()), message_thread_id=constants.TELEGRAM_GATHER_SQUAD_TOPIC_ID)
        log("[Automated message] 📝 Start of registration message sent out.")
    except Exception as e:
        log_error(e)


def start_waking_up():
    try:
        bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, "💤 Просыпаемся! /wakeup", message_thread_id=constants.TELEGRAM_GAMEDAY_TOPIC_ID)
        log("[Automated message] 💤 Start of waking message sent out.")
    except Exception as e:
        log_error(e)


def good_morning():
    try:
        weather = Weather()
        weather_forecast = weather.get_forecast()

        bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, str(weather_forecast), parse_mode='MarkdownV2')

        log(f"Good morning message sent out. Weather: {weather_forecast}")

    except Exception as e:
        log_error(e)

def pitch_payment_reminder():
    try:
        games_since_last_layment_for_pitch = database.how_many_games_since_last_layment_for_pitch()
        date_of_last_layment_for_pitch = format_date(database.date_of_last_layment_for_pitch())
        how_much_we_owe = games_since_last_layment_for_pitch * constants.COST_OF_1_GAME
        message_text = f"💵 Напоминка про оплату за поле.\nПоследний раз мы платили за поле {date_of_last_layment_for_pitch}.\nС момента последней оплаты прошло {games_since_last_layment_for_pitch} игр (в том числе считая следующую субботу).\n💲Сумма к оплате: {how_much_we_owe} р."
        bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, message_text, message_thread_id=constants.TELEGRAM_ACCOUNTING_TOPIC_ID)
        log("Pitch payment reminder sent out.")
    except Exception as e:
        log_error(e)

def daily_backup():
    try:
        backuper = Database_backup()
        backuper.backup_table("players")
        backuper.backup_table("games")
        backuper.backup_table("matchday")
        log("✅💿 Database backup successfully created")
    except Exception as e:
        log_error(e)

def shutdown():
    if scheduler is not None:
        scheduler.shutdown()
