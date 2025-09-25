import requests
from helpers import fill_template, get_today_minsk_time
from dotenv import load_dotenv
import os

load_dotenv()
API_NINJAS_API_TOKEN = os.environ['API_NINJAS_API_TOKEN']

class RandomFactsClient:
    def __init__(self):
        self.BASE_URL = "https://api.api-ninjas.com/v1/historicalevents?month={month}&day={day}"
        
    def get_random_fact(self):
        PARAMS = {'key':self.BASE_URL}

        date = get_today_minsk_time()
        
        modified_URL = fill_template(self.BASE_URL, month = date.month, day = date.day)

        response = requests.get(url=modified_URL, params=PARAMS, headers={"X-Api-Key": API_NINJAS_API_TOKEN}).json()
        latest_id = len(response) - 1
        year = response[latest_id]["year"]
        event = response[latest_id]["event"]
        random_event = f"{year} year: {event}"

        return random_event