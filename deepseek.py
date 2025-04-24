import os
from dotenv import load_dotenv
from openai import OpenAI
import constants

load_dotenv()
DEEPSEEK_API_KEY = os.environ['DEEPSEEK_API_KEY']

conversation_id = None

def send_request(prompt, temperature):
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

    with open(constants.SYSTEM_PROMPT_FILENAME,"r") as system_prompt_file:
            system_prompt = system_prompt_file.read()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        stream=False,
        conversation_id = conversation_id
    )

    if conversation_id == None:
        conversation_id = response.get("conversation_id")
        print(conversation_id)

    return response.choices[0].message.content