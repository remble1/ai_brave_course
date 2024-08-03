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
    print(question, "<- pytanie")
    # powiedz mi, gdzie mieszka Katarzyna Truskawka? w jakim mieście?

    client = OpenAI(api_key=open_api_key)

    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"""
            Aby odpoweidzieć na to pytanie określ jakich danych potrzebujesz i kogo one dotyczną.
            Twoja odpowiedź ma być w formacie JSON:
            
            Przykładowe pytanie:
            powiedz mi, gdzie mieszka Tomek Ananas? w jakim mieście?
            Twoja odpowiedź:
            {{"imie": "Tomek",
              "nazwisko": "Ananas",
              "pytanie": "miasto"}}
            
            Przykładowe pytanie:
            powiedz mi, jaki jest ulubiony kolor Mariusza Zorro?
            Twoja odpowiedź:
            {{"imie": "Mariusz",
              "nazwisko": "Zorro",
              "pytanie": "ulubiony_kolor"}}
              
            Przykładowe pytanie:
            powiedz mi, jaki jest ulubiony film Magdy Truskawka?
            Twoja odpowiedź:
            {{"imie": "Magda",
              "nazwisko": "Truskawka",
              "pytanie": "ulubiony_film"}}
              
            Przykładowe pytanie:
            powiedz mi, jaki jest ulubiony serial Krysia Ludek?
            Twoja odpowiedź:
            {{"imie": "Krystyna",
              "nazwisko": "Ludek",
              "pytanie": "ulubiony_serial"}}  
                
            question: {question}
            
            
         """}
    ]
    )
    
    res = completion.choices[0].message.content
    res_json = json.loads(res)
    
    print(res, "<- odpowiedz")

    with open('data_qdrant_json/archiwum_people.json', 'r') as f:
        data = json.load(f)

        
    found_entry = None

    for entry in data:
        
        if entry.get('imie') == res_json['imie'] and entry.get('nazwisko') == res_json['nazwisko']:
            found_entry = entry
            break  # Jeśli znaleziono dopasowanie, przerwij pętlę

    if found_entry:
        print("Znaleziono wpis:")
        # print(found_entry)
    else:
        print(f"Nie znaleziono wpisu dla imienia {res_json['imie']} i nazwiska {res_json['nazwisko']}.")
        
    if res_json['pytanie'] == 'miasto':
        print(found_entry['o_mnie'])
        
        completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"""
                Wydobądź nazwę miasta z tego zdania. 
                Przykład: 
                Mieszkam we Wrocławiu
                Twoja odpowiedź:
                Wrocław
                Przykład:
                Zamieszkuję w Bydgoszu
                Twoja odpowiedź:
                Bydgoszcz
                question: {found_entry['o_mnie']}
            """}
        ]
        )
        
        res = completion.choices[0].message.content
        print(res)
        return res
        
        
        
    if res_json['pytanie'] == 'ulubiony_kolor':
        print(found_entry['ulubiony_kolor'])
        return found_entry['ulubiony_kolor']
        



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
    token = get_token("people")
    payload = get_task(token)
    send_task(token, payload)
    