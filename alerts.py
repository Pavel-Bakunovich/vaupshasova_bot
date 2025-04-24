from apscheduler.schedulers.background import BackgroundScheduler
import os
import telebot
import deepseek
import constants
from logger import log, log_error
from pytz import timezone
from helpers import get_next_matchday_formatted, fill_template

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
    scheduler.add_job(random_abusive_comment,
                      'cron',
                      hour=8,
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


def random_abusive_comment():
    try:
        with open(constants.MAKSIM_JOKE_PROMPT_TEMPLATE_FILENAME,"r") as maksim_joke_prompt_template_file:
            maksim_joke_prompt_template_text = maksim_joke_prompt_template_file.read()

        response = deepseek.send_request(maksim_joke_prompt_template_text, 1.5)
        bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, str(response))
        log("[Automated message] Random abusive comment sent out.")
    except Exception as e:
        log_error(e)
    
def shutdown():
    if scheduler is not None:
        scheduler.shutdown()
