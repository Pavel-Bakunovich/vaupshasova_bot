import requests
from helpers import fill_template, get_today_minsk_time

class NumbersAPIClient:
    def __init__(self):
        self.BASE_URL = "http://numbersapi.com/{month}/{day}/date"
    def get_random_fact(self):
        PARAMS = {'key':self.BASE_URL}

        date = get_today_minsk_time()
        
        modified_URL = fill_template(self.BASE_URL, month = date.month, day = date.day)

        response = requests.get(url = modified_URL, params = PARAMS)

        return response.text