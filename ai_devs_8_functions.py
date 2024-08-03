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


    question = 'Pawel, Sadkowski, 1997'
    data = {'question': question}       
    response = requests.post(url, data=data)
            
    client = OpenAI(api_key=open_api_key)

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": f"""
        Your response must be in form:
            {{
                    "name": "addUser",
                    "description": "add new user to the database",
                    "parameters": {{
                        "type": "object",
                        "properties": {{
                            "name": {{
                                "type": "string",
                                "description": "provide name of the user"
                            }},
                            "surname" : {{
                                "type": "string",
                                "description": "provide surname of the user"
                            }},
                            "year" : {{
                                "type": "number",
                                "description": "provide year of birth of the user"
                            }}
                        }}
                    }}
                }}
            
            take paremeters, fill json and give me back:
            parameters: {question}"""
            }])
            
    
    res = completion.choices[0].message.content
    return res


def send_task(token, payload):
    answer = {
        "answer": payload
    }
    json_data = json.dumps(answer)
    print(answer)
    url = f"{answer_path}{token}"
    
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        print("rezultat po zaladowaniu zadania", response.json())
    else:
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    token = get_token("functions")
    payload = get_task(token)
    send_task(token, payload)
    