import requests
import json
from openai import OpenAI
import os

ai_devs_token = os.getenv('AI_DEV_KEY')
token_path = os.getenv('TOKEN_PATH')
task_path = os.getenv('TASK_PATH')
answer_path = os.getenv('ANSWER_PATH')
open_api_key = os.getenv('OPENAI_API_KEY')
#moderation

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
    
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("task", response.json())
    else:
        print("Err:", response.status_code)
    
    a = response.json()['blog']
    
    payload_list = []
    for line in a:
            
        client = OpenAI(api_key=open_api_key)

        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś specjalistą do tworzenia wpisów do kulinarnego bloga. Oto Twoja instrukcja o czym powinien być wpis:"},
            {"role": "user", "content": line}
        ]
        )
        print(completion.choices[0].message.content)
        payload_list.append(completion.choices[0].message.content)
        
    
    return payload_list

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
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    token = get_token("blogger")
    payload = get_task(token)
    send_task(token, payload)