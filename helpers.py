import datetime
import calendar
import locale

def fill_template(template, **kwargs):
  result = template
  for key, value in kwargs.items():
    placeholder = f"{{{key}}}"
    result = result.replace(placeholder, str(value))
  return result


def get_next_matchday():
  today = datetime.date.today()  #reference point.
  saturday = today + datetime.timedelta(
      (calendar.SATURDAY - today.weekday()) % 7)
  return saturday


def get_next_matchday_formatted():

  MONTHS_RU = {
    1: 'янв', 2: 'фев', 3: 'мар', 4: 'апр', 5: 'мая', 6: 'июн',
    7: 'июл', 8: 'авг', 9: 'сен', 10: 'окт', 11: 'ноя', 12: 'дек'
  }
  date = get_next_matchday()
  return f"{date.day} {MONTHS_RU[date.month]} {date.year}"
  #return get_next_matchday().strftime(format='%d %b %Y')


def allow_registration():
  if (datetime.date.today().weekday() == 5) or (datetime.date.today().weekday() == 6):
    return False
  else:
    return True
