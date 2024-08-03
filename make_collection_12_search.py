from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema.document import Document
import qdrant_client
import os
import uuid
import json

# before run, turn on dockers -> docker compose up -d 
qdrant_collection_name = "my_collection"

def load_points():
        
    with open('data_qdrant/archiwum_aidevs.json', 'r') as f:
        data = json.load(f)


    embeddings = OpenAIEmbeddings()
    url = "http://localhost:6333/"
    docs = []
    for i in data:
        myuuid = uuid.uuid4()
        myuuidStr = str(myuuid)
        
        doc = Document(
            page_content = i['info'],
            metadata = {"id": myuuidStr,
                        "title": i['title'],
                        "url": i['url'],
                        "date": i['date']}
        )
        docs.append(doc)
        
    Qdrant.from_documents(
        docs,
        embeddings,
        url=url,
        prefer_grpc=True,
        collection_name=qdrant_collection_name,
    )
        
if __name__ == '__main__':
    load_points()
    pass