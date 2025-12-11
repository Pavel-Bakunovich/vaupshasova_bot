import constants
import os
from helpers import get_next_matchday, get_today_minsk_time_formatted, fill_template,get_today_minsk_time
import deepseek
from logger import log, log_error
import database
import io

class HotStatsGenerator:
    def __init__(self):
        pass

    def get_message(self):    
        #with open(constants.GOOD_MORNING_PROMPT_TEMPLATE_FILENAME,"r") as good_morning_prompt_template_file:
        #    good_morning_prompt_template_text = good_morning_prompt_template_file.read()

        response = deepseek.send_request("Напиши сообщение игрокам, что скоро ровно в это время каждый день будет появляться интересная статистика. Пообещай с приколом, что скоро будет. Хоть будет не скоро. Не здоровайся. Сообщение короткое - не больше 3-4 предложений.", 0)

        return response

    