from apscheduler.schedulers.background import BackgroundScheduler
import os
import telebot
import deepseek
import constants
from logger import log, log_error
from pytz import timezone
from helpers import get_next_matchday_formatted, fill_template
import requests

WEATHER_API_KEY = os.environ['WEATHER_API_TOKEN']
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
        base_URL="http://api.weatherapi.com/v1/forecast.json" 
        PARAMS = {'key':WEATHER_API_KEY,
                    'q':"Minsk",
                    'days':1,
                    'aqi':"no",
                    'alerts':"no"}
    
        with open(constants.GOOD_MORNING_PROMPT_TEMPLATE_FILENAME,"r") as good_morning_prompt_template_file:
            good_morning_prompt_template_text = good_morning_prompt_template_file.read()

        with open(constants.WEATHER_FORECSAT_TEMPLATE_FILENAME,"r") as weather_forecsat_template_file:
            weather_forecsat_template_text = weather_forecsat_template_file.read()

        response = requests.get(url = base_URL, params = PARAMS)

        weather_forecast = response.json()

        weather_forecast_text = fill_template(weather_forecsat_template_text,
                                        temp_c = weather_forecast['current']['temp_c'],
                                        feelslike_c = weather_forecast['current']['feelslike_c'],
                                        condition_now = weather_forecast['current']['condition']['text'],
                                        wind_kph = weather_forecast['current']['wind_kph'],
                                        gust_kph = weather_forecast['current']['gust_kph'],
                                        wind_dir = weather_forecast['current']['wind_dir'],
                                        pressure_mb = weather_forecast['current']['pressure_mb'],
                                        precip_mm = weather_forecast['current']['precip_mm'],
                                        cloud = weather_forecast['current']['cloud'],
                                        humidity = weather_forecast['current']['humidity'],
                                        vis_km = weather_forecast['current']['vis_km'],
                                        uv_now = weather_forecast['current']['uv'],
                                        maxtemp_c = weather_forecast['forecast']['forecastday'][0]['day']['maxtemp_c'],
                                        mintemp_c = weather_forecast['forecast']['forecastday'][0]['day']['mintemp_c'],
                                        avgtemp_c = weather_forecast['forecast']['forecastday'][0]['day']['avgtemp_c'],
                                        maxwind_kph = weather_forecast['forecast']['forecastday'][0]['day']['maxwind_kph'],
                                        totalprecip_mm = weather_forecast['forecast']['forecastday'][0]['day']['totalprecip_mm'],
                                        totalsnow_cm = weather_forecast['forecast']['forecastday'][0]['day']['totalsnow_cm'],
                                        avgvis_km = weather_forecast['forecast']['forecastday'][0]['day']['avgvis_km'],
                                        avghumidity = weather_forecast['forecast']['forecastday'][0]['day']['avghumidity'],
                                        daily_will_it_rain = weather_forecast['forecast']['forecastday'][0]['day']['daily_will_it_rain'],
                                        daily_chance_of_rain = weather_forecast['forecast']['forecastday'][0]['day']['daily_chance_of_rain'],
                                        daily_will_it_snow = weather_forecast['forecast']['forecastday'][0]['day']['daily_will_it_snow'],
                                        daily_chance_of_snow = weather_forecast['forecast']['forecastday'][0]['day']['daily_chance_of_snow'],
                                        uv = weather_forecast['forecast']['forecastday'][0]['day']['uv'],
                                        condition = weather_forecast['forecast']['forecastday'][0]['day']['condition']['text'],
                                        moon_phase = weather_forecast['forecast']['forecastday'][0]['astro']['moon_phase'],
                                        sunrise = weather_forecast['forecast']['forecastday'][0]['astro']['sunrise'],
                                        sunset = weather_forecast['forecast']['forecastday'][0]['astro']['sunset'],
                                        moonrise = weather_forecast['forecast']['forecastday'][0]['astro']['moonrise'],
                                        moonset =weather_forecast['forecast']['forecastday'][0]['astro']['moonset'])
        response = deepseek.send_request(fill_template(good_morning_prompt_template_text, weather_forecast=weather_forecast_text), 1.5)

        bot.send_message(constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID, str(response))

        log(fill_template("[Automated message] Good morning message sent out. Weather: {weather}", weather=weather_forecast_text))

    except Exception as e:
        log_error(e)
    
def shutdown():
    if scheduler is not None:
        scheduler.shutdown()
