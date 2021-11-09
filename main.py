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
from backend.util import *

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
client = MongoClient(mongo_uri)

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
    existing_user = check_user(data["email"])

    if existing_user == True:
        return "Email already registered, try again with another email"

    if data["pswd"] != data["cpswd"]:
        return "Passwords don't match, try again"
    else:
        enc_pswd = encrypt_password(data["pswd"])

    try:
        add_to_mongo(data, enc_pswd)
    except:
        raise ConnectionError

    if ConnectionError:
        return "Something went wrong, please try again"
    else:
        return "user created successfully, login with same credentials."
