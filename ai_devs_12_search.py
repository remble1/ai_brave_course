import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from openai import OpenAI
load_dotenv()
from qdrant_client import models, QdrantClient
llm = ChatOpenAI()
from langchain.embeddings.openai import OpenAIEmbeddings
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

def get_task(token):
    url = f"{task_path}{token}"
    
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("task", response.json())
        ...
    else:
        print("Err:", response.status_code)

    question = response.json()['question']
    embeddings = OpenAIEmbeddings()
    embedded_query = embeddings.embed_query(question)

    client = QdrantClient(url="http://localhost:6333")

    hits = client.search(
        collection_name="my_collection",
        query_vector=embedded_query,
        limit=1,
    )
    print(hits)
    print(hits[0].payload['metadata']['url'], "<- res")
    return hits[0].payload['metadata']['url']
    

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
    token = get_token("search")
    payload = get_task(token)
    send_task(token, payload)
    