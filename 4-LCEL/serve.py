from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="llama-3.3-70b-versatile",groq_api_key=groq_api_key)

system_temp="Translate the following into {language}:"
prompt_temp= ChatPromptTemplate.from_messages([
    ("system",system_temp),("user","{text}")
])

parser=StrOutputParser()

chain=prompt_temp|model|parser

##App definition
app=FastAPI(title="Langchain Server",
            version="1.0",
            description="A simple API server")

## Adding chain routes
add_routes(
    app,
    chain,path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
