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
from qdrant_client import models, QdrantClient
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

    question = response.json()['question']
    
    client = OpenAI(api_key=open_api_key)
    
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"""
            Otrzymasz pytanie, musisz stwierdzić na jaki temat ono jest
            
            Gdy pytanie dotyczy waluty odpowiedz:
            
            Jaka jest aktualna wartość euro.
            Odpowiedz:
            {{"type": "currency",
              "currency": "EUR"}}    
        
            Gdy pytanie dotyczy populacji Niemiec 
            {{"type": "population",
              "currency": "niemcy"}} 
            
            jeśli pytanie dotyczy czegoś innego niż tego wymienionego wyżej odpoweidz na nie ale w formie zwykłego zdania.
        
            question: {question}
        """}
    ]
    )
    
    res = completion.choices[0].message.content
    res_json = json.loads(res)
    
    if res_json['type'] == "currency":
        table_type = 'A'  
        currency_code = res_json['currency']  
        exchange_rate = get_exchange_rate(table_type, currency_code)
        if exchange_rate:
            print(f"Wartość {currency_code} w tabeli {table_type}: {exchange_rate}")
            return(exchange_rate)
        else:
            print(f"Nie udało się znaleźć kursu waluty {currency_code} w tabeli {table_type}.")
    
    
    print(res)
    
    if res_json['type'] == "population":
        pass

    else: 
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
    token = get_token("knowledge")
    payload = get_task(token)
    send_task(token, payload)
    