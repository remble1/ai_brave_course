import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI
load_dotenv()
llm = ChatOpenAI()
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import json
llm = ChatOpenAI()
import requests
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

    msg = response.json()["msg"]
    hint = response.json()["hint"]
    question = response.json()["question"]
    
    client = OpenAI(api_key=open_api_key)
    
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"""
            Musisz wybierać odpowiednie wartości jsonów bazując na kontekście dostarczonego rozkazu.
            Przykład:
            Przypomnij mi, że mam kupić mleko
            Twoja odpowiedź:
            {{"tool":"ToDo","desc":"Kup mleko"}}

            Przykład:
            Jutro mam spotkanie z Marianem 
            Twoja odpowiedź:
            {{"tool":"Calendar","desc":"Spotkanie z Marianem","date":"2024-05-03"}}

            Dzisiejsza data to 02.05.2024

            question: {question}
        """}
    ]
    )
    
    res = completion.choices[0].message.content
    res_json = json.loads(res)
    print(res_json)
    return res_json
    # 'always use YYYY-MM-DD format for dates', 'example for ToDo': 'Przypomnij mi, że mam kupić mleko = {"tool":"ToDo","desc":"Kup mleko" }'
    # Przykładowe wywołanie funkcji





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
    token = get_token("tools")
    payload = get_task(token)
    send_task(token, payload)
    