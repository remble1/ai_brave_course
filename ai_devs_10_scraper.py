import requests
import json
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
from dotenv import load_dotenv
load_dotenv()
import time
import random
#moderation
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
    
    response = requests.get(url, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("task", response.json())
        ...
    else:
        print("Err:", response.status_code)

    response_obj = response.json()
    data_url = response_obj['input']
    
    while True:
        time.sleep(random.randint(2, 5))

        response = requests.get(data_url, timeout=60, headers={"User-Agent": "Chrome"})

        if response.status_code == 200 or response.status_code == 403 or response.status_code == 500:
            
            print(response.text, "elo")
            
            if response.text == "server error X_X":
                continue
            
            llm = ChatOpenAI()

            msg = response_obj['msg']
            question = response_obj['question']
                    
            client = OpenAI(api_key=open_api_key)

            prompt = ChatPromptTemplate.from_messages(
                [("system", """You will get a description of different people 
                                Understand exactly who is who
                                what they do
                                what their descriptions are
                                And then perfectly answer the question asked.
                                Answer as short as possible.
                                <<{question}>>
                                <<{context}>>
                                """)]
            )
            llm = ChatOpenAI(model_name="gpt-4-turbo-preview")
            chain = create_stuff_documents_chain(llm, prompt)

            docs = [Document(page_content=value) for value in response.text]

            res = chain.invoke({"context": docs, "question": question})
            
            print(res)
            return(res)
            
        else:
            print("Błąd pobierania zawartości strony:", response.status_code)
        

        





def send_task(token, payload):
    answer = {
        "answer": payload
    }
    json_data = json.dumps(answer)
    
    url = f"https://tasks.aidevs.pl/answer/{token}"
    
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("rezultat po zaladowaniu zadania", response.json())
    else:
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    token = get_token("scraper")
    payload = get_task(token)
    send_task(token, payload)