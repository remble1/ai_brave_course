import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
load_dotenv()
import time
llm = ChatOpenAI()
import os

ai_devs_token = os.getenv('AI_DEV_KEY')
token_path = os.getenv('TOKEN_PATH')
task_path = os.getenv('TASK_PATH')
answer_path = os.getenv('ANSWER_PATH')
open_api_key = os.getenv('OPENAI_API_KEY')

def get_token(task_name):
    data = {
        "apikey": ai_devs_token
    }
    url = f"{token_path}{task_name}"
    json_data = json.dumps(data)
    
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        token = response.json()['token']
        print(token)
        return token
    else:
        print("Err:", response.status_code)
        return "err"

def get_task(token):
    url = f"{task_path}{token}"
    
    full_sentence = ""
    while True:
        time.sleep(2)
        response = requests.get(url, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            ...
        else:
            print("Err:", response.status_code)
        
        hints_bag = response.json()['hint'] + " "
        full_sentence += hints_bag 
        
        client = OpenAI(api_key=open_api_key)

        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''Poniżej otrzymasz zdania opisujące pewną osobę, jeżeli jest pewny na 100 procent o kim jest mowa odpisz wiadomośc w fomie JSON {"sure": "yes", "person": "wybrana przez Ciebie osoba"}, jeżeli nie wiesz o kim jest mowa odpisz mi wiadomość {"sure": "no", "person": "None"}'''},
            {"role": "user", "content": full_sentence}
        ]
        )
        
        res = completion.choices[0].message.content
        print(res)
        json_obj = json.loads(res)
        if json_obj['sure'] == "yes":
            return json_obj['person']
        
        continue
        


def send_task(token, payload):
    answer = {
        "answer": payload
    }
    json_data = json.dumps(answer)
    
    url = f"{answer_path}{token}"
    
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("rezultat po zaladowaniu zadania", response.json())
    else:
        print(response.json())

if __name__ == "__main__":
    token = get_token("whoami")
    payload = get_task(token)
    send_task(token, payload)