import datetime
import calendar
import constants
import pytz
import re

def fill_template(template, **kwargs):
  result = template
  for key, value in kwargs.items():
    placeholder = f"{{{key}}}"
    result = result.replace(placeholder, str(value))
  return result

def get_today_minsk_time():
  tz = pytz.timezone('Europe/Minsk')
  today_minsk = datetime.datetime.now(tz)
  return today_minsk

def get_today_minsk_time_formatted():
  return format_date(get_today_minsk_time())

def get_next_matchday():
  today_minsk = get_today_minsk_time()
  saturday = today_minsk + datetime.timedelta((calendar.SATURDAY - today_minsk.weekday()) % 7)
  saturday = saturday.replace(hour=8, minute=30, second=0, microsecond=0)
  return saturday

def get_next_matchday_formatted():
  return format_date(get_next_matchday())

def format_date(date):
  MONTHS_RU = {
    1: 'янв', 2: 'фев', 3: 'мар', 4: 'апр', 5: 'мая', 6: 'июн',
    7: 'июл', 8: 'авг', 9: 'сен', 10: 'окт', 11: 'ноя', 12: 'дек'
  }
  return f"{date.day} {MONTHS_RU[date.month]} {date.year}"

def get_day_of_week():
  date = get_today_minsk_time()
  day_of_week = date.weekday()  # Returns 0 (Monday) to 6 (Sunday)
  # Map weekday numbers to Russian day names
  russian_days = {
      0: "понедельник",
      1: "вторник", 
      2: "среда",
      3: "четверг",
      4: "пятница",
      5: "суббота",
      6: "воскресенье"
  }
  return russian_days[day_of_week]

def allow_registration():
  today_minsk = get_today_minsk_time()
  # Registration  is not allowed on Saturdays, Sundays, and before 8 AM on Mondays
  if (today_minsk.weekday() == 5) or (today_minsk.weekday() == 6) or ((today_minsk.weekday() == 0) and (today_minsk.hour < 8)):
    return False
  else:
    return True

def authorized(chat_id):
  # This magic number is an ID of our the "Лига Ваупшасова" group chat. 
  # People can use this bot from withit either exclusively this group or in personal chat. This bot cannot be used in another group chat.
  if chat_id == constants.VAUPSHASOVA_LEAGUE_TELEGRAM_ID or chat_id > 0:
    return True
  else:
    return False
  
def is_CEO(telegram_id):
  return telegram_id == constants.CEO_TELEGRAM_ID

def get_arguments(input):
    parts = input.split(' ', 1)
    if len(parts) > 1:
        return parts[1]
    else:
        return None
    
def escape_markdown(text):
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)