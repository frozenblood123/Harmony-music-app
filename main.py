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


class login_data(BaseModel):
    email: str
    pswd: str

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
        return "user created successfully, login with same credentials."

    except ConnectionError:
        return "Something went wrong, please try again"


@app.post("/login/")
def login(data: login_data):
    data = data.dict()
    existing_user = check_user(data["email"])

    if existing_user == False:
        return "This email has not been registered. Please signup before logging in"
    elif existing_user == True:
        verification = verify_password(
            data["pswd"], get_password(data["email"]))
        if verification == True:
            return "Login successful"
        else:
            return "Incorrect password"
    else:
        return "Something went wrong"
