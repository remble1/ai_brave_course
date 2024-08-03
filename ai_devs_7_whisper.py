import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI
from openai import OpenAI
load_dotenv()
import os

ai_devs_token = os.getenv('AI_DEV_KEY')
token_path = os.getenv('TOKEN_PATH')
task_path = os.getenv('TASK_PATH')
answer_path = os.getenv('ANSWER_PATH')
open_api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI()

def get_token(task_name):
    data = {
        "apikey": ai_devs_token
    }
    url = f"{ai_devs_token}{task_name}"
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
        ...
    else:
        print("Err:", response.status_code)

    file_name = "data/mateusz.mp3"
    
        
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    audio_file= open(file_name, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return(transcription.text)

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
    token = get_token("whisper")
    payload = get_task(token)
    send_task(token, payload)
    