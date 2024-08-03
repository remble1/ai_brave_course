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
        # print("task", response.json())
        ...
    else:
        # print("Err:", response.status_code)
        ...

    import base64
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    pic_url = "documents/6.jpg"
    base64_image = encode_image(pic_url)


    client = OpenAI(api_key=open_api_key)

    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "List the contents of this document, translated into English."},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
            },
            },
        ],
        }
    ],
    max_tokens=4000,
    )

    print(response.choices[0].message.content)




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
    token = get_token("gnome")
    payload = get_task(token)
    # send_task(token, payload)
    