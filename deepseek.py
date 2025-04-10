import os
from dotenv import load_dotenv
from openai import OpenAI
import constants

load_dotenv()
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

def send_request(prompt, temperature):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": constants.SYSTEM_PROMPT_DEEPSEEK},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        stream=False
    )

    return response.choices[0].message.content