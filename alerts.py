from apscheduler.schedulers.background import BackgroundScheduler
import os
import telebot
import deepseek
import constants
from logger import log
from pytz import timezone

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
    scheduler.add_job(randon_abusive_comment,
                      'cron',
                      hour=8,
                      minute=0,
                      timezone=timezone('Europe/Minsk'))

    scheduler.start()


def start_registration():
    bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, "📝 Погнали регистрироваться! /add", message_thread_id=30988)
    log("[Automated message] Start of registration message sent out.")


def start_waking_up():
    bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, "💤 Просыпаемся! /wakeup", message_thread_id=30990)
    log("[Automated message] Start of waking message sent out.")


def randon_abusive_comment():
    response = deepseek.send_request(constants.RANDOM_MAKSIM_JOKE_PROMPT_DEEPSEEK, 1)
    bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, str(response))
    log("[Automated message] Random abusive comment sent out.")


def shutdown():
    if scheduler is not None:
        scheduler.shutdown()
