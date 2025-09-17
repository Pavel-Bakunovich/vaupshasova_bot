import constants
import os
import requests
from helpers import get_next_matchday_formatted, get_today_minsk_time_formatted, fill_template,format_date
import deepseek
from logger import log, log_error
import command_records

class GoodMorningMessage:
    def __init__(self):
        self.WEATHER_API_KEY = os.environ['WEATHER_API_TOKEN']
    def get(self):
        base_URL="http://api.weatherapi.com/v1/forecast.json" 
        PARAMS = {'key':self.WEATHER_API_KEY,
                    'q':"Minsk",
                    'days':1,
                    'aqi':"no",
                    'alerts':"no"}
    
        with open(constants.GOOD_MORNING_PROMPT_TEMPLATE_FILENAME,"r") as good_morning_prompt_template_file:
            good_morning_prompt_template_text = good_morning_prompt_template_file.read()
        '''
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
        log(f"Weather: {weather_forecast_text}")
        
        stats = command_records.build_records_text()
        '''
        #response = deepseek.send_request(fill_template(good_morning_prompt_template_text, weather_forecast = weather_forecast_text, stats = stats, date = get_today_minsk_time_formatted()), 1.5)
        response = deepseek.send_request(good_morning_prompt_template_text, 0)

        return response