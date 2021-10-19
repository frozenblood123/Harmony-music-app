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

# connect mongoDB
load_dotenv()
mongo_uri = os.getenv("mongo_uri")
print(mongo_uri)
client = MongoClient(
    "mongodb+srv://harsh:harsh@cluster0.2i28j.mongodb.net/harmony_users?retryWrites=true&w=majority")

# add db
db = client.get_database("harmony_users")
# add collection
profile = db.user_profile


@app.get('/')
def index():
    message = "Harmony is live!"
    return message


class signup_data(BaseModel):
    firstname: str
    lastname: str
    dob: str
    email: str
    pswd: str
    cpswd: str


@app.post("/signup/")
def signup(data: signup_data):
    data = data.dict()
    print(data)
    profile.insert_one(data)
    return "user created successfully, login with same credentials."
