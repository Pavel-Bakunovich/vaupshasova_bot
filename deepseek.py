import os
from dotenv import load_dotenv
from openai import OpenAI
import constants

load_dotenv()
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

with open(constants.SYSTEM_PROMPT_FILENAME,"r") as system_prompt_file:
            system_prompt = system_prompt_file.read()

messages = [{"role": "system", "content": system_prompt}]

def send_request(prompt, temperature):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=temperature,
        stream=False
    )

    messages.append(response.choices[0].message)

    return response.choices[0].message.content