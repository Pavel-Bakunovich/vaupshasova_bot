import os
from dotenv import load_dotenv
from openai import OpenAI
from helpers import get_day_of_week, get_today_minsk_time_formatted, fill_template
import constants

load_dotenv()
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

def get_refreshed_system_prompt():
    with open(constants.SYSTEM_PROMPT_FILENAME,"r") as system_prompt_file:
        system_prompt = system_prompt_file.read()
    system_prompt = fill_template(system_prompt, day_of_week=get_day_of_week(), date=get_today_minsk_time_formatted())
    return system_prompt

system_prompt = get_refreshed_system_prompt()

messages = [{"role": "system", "content": system_prompt}]

def send_request(prompt, temperature):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    messages[0]["content"] = get_refreshed_system_prompt()

    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=temperature,
        stream=False
    )

    messages.append(response.choices[0].message)

    return response.choices[0].message.content

