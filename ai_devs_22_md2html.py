import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI
import pandas
load_dotenv()
llm = ChatOpenAI()
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
import json
llm = ChatOpenAI()
import requests
from openai import OpenAI
import os

ai_devs_token = os.getenv('AI_DEV_KEY')
token_path = os.getenv('TOKEN_PATH')
task_path = os.getenv('TASK_PATH')
answer_path = os.getenv('ANSWER_PATH')
open_api_key = os.getenv('OPENAI_API_KEY')
# before working on qdarnt db run docker compose up -d

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
    
    
def get_exchange_rate(table_type, currency_code):
    url = f"http://api.nbp.pl/api/exchangerates/tables/{table_type}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for table in data:
            for rate in table['rates']:
                if rate['code'] == currency_code:
                    return rate['mid']
    else:
        print("Err pull data from server")

def get_task(token):
    url = f"{task_path}{token}"
    
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("task", response.json())
        ...
    else:
        print("Err:", response.status_code)


    _input = response.json()['input']
    _msg = response.json()['msg']
    
    client = OpenAI(api_key=open_api_key)

    response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal:md-html:xxxxxx",
    messages=[
        {"role": "system", "content": f"""
            {_msg}
            
            Pamiętaj o zasadzie:
            **verb** = <span class="bold">verb</span>
                       
            Markdown: {_input}
        """}
    ],
    max_tokens=300,
    )
    
    res = response.choices[0].message.content
    print(res)
    return res



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
    token = get_token("md2html")
    payload = get_task(token)
    send_task(token, payload)
    