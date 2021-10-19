import os
import uvicorn
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Harmony the music friend",
    description="Harmony is live. Play any music you like among other thing! go to /docs")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#connect mongoDB
load_dotenv()
mongo_uri = os.getenv("mongo_uri")
client = MongoClient(mongo_uri)

#add db
db = client.get_database("harmony_users")
#add collection
profile = db.user_profile


@app.get('/')
def index():
    message = "Harmony is live!"
    return message
