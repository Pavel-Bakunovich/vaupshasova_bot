import datetime
import calendar
import pytz

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

def get_next_matchday():
  today_minsk = get_today_minsk_time()
  saturday = today_minsk + datetime.timedelta((calendar.SATURDAY - today_minsk.weekday()) % 7)
  return saturday

def get_next_matchday_formatted():

  MONTHS_RU = {
    1: 'янв', 2: 'фев', 3: 'мар', 4: 'апр', 5: 'мая', 6: 'июн',
    7: 'июл', 8: 'авг', 9: 'сен', 10: 'окт', 11: 'ноя', 12: 'дек'
  }
  date = get_next_matchday()
  return f"{date.day} {MONTHS_RU[date.month]} {date.year}"

def allow_registration():
  today_minsk = get_today_minsk_time()
  if (today_minsk.weekday() == 5) or (today_minsk.weekday() == 6):
    return False
  else:
    return True

