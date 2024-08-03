import requests
import json
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

    content = response.json()['input']
    
    url = 'https://api.openai.com/v1/moderations'
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {open_api_key}'
    }
    answer_list = []
    
    for i in content:
        data = {
        'input': i
        }
        
        response = requests.post(url, headers=headers, json=data)
        a = response.json()['results'][0]['flagged']
        print(a)
        if a == True:
            answer_list.append("1")
        if a == False:
            answer_list.append("0")
    
    return answer_list

def send_task(token, payload):
    
    answer = {
        "answer": payload
    }
    json_data = json.dumps(answer)
    
    url = f"{answer_path}{token}"
    
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("rezultat po zaladowaniu zadania", response.json())

if __name__ == "__main__":
    token = get_token("moderation")
    payload = get_task(token)
    send_task(token, payload)