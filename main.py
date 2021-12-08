import os
import uvicorn
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from starlette.responses import Response
from fastapi import FastAPI, Depends, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi_login import LoginManager
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

class user_data(BaseModel):
    email: str

class PlaylistData(BaseModel):
    playlist_name: str
    songs: list

class SongData(BaseModel):
    name: str
    type: str

@app.post("/signup/")
def signup(data: signup_data):
    data = data.dict()
    existing_user = check_user(data["email"])

    if existing_user == True:
        print("already exists")
        return "Email already registered, try again with another email"

    if data["pswd"] != data["cpswd"]:
        return "Passwords don't match, try again"
    else:
        enc_pswd = encrypt_password(data["pswd"])

    try:
        add_to_mongo(data, enc_pswd)
        print("signup_successful")
        return "user created successfully, login with same credentials."

    except ConnectionError:
        return "Something went wrong, please try again"


SECRET = "800c17d0d605de7277d95019b816b2dd0736ec3cad4e0145"
manager = LoginManager(SECRET, token_url='/login/', use_cookie=True)


@manager.user_loader()
def load_user(email: str):
    user = email
    return user


@app.post("/login/")
def login(data: login_data, response: Response):
    data = data.dict()
    existing_user = check_user(data["email"])
    user = load_user(data["email"])
    if existing_user == False:
        return "This email has not been registered. Please signup before logging in"
    elif existing_user == True:
        verification = verify_password(
            data["pswd"], get_password(data["email"]))
        if verification == True:
            access_token = manager.create_access_token(
                data={'sub': data['email']}, expires=timedelta(days=365))
            #response = RedirectResponse(url='/dashboard', status_code=status.HTTP_302_FOUND)
            manager.set_cookie(response, access_token)
            #resp = RedirectResponse(url="/home-page")
            #return resp
            return "Login successful"
            #return {'access_token': access_token, 'token_type': 'bearer'}
        else:
            return "Incorrect password"
    else:
        return "Something went wrong"


@app.get('/home-page')
def protected_route(user=Depends(manager)):
    return "Logged in successfully"


@app.get("/logout")
async def logout(request: Request, response: Response, user=Depends(manager)):
    print(manager("access_token"))
    response.delete_cookie("access_token")
    return "logged out"


@app.post('/get-user/')
async def get_user(data: user_data):
    data = data.dict()
    user = load_user(data["email"])
    user_email = user
    user_info = get_user_info(user_email)
    return user_info


@app.get('/search-song/')
async def search_song(data:SongData, user=Depends(manager)):
    data = data.dict()
    search_name = data["name"]
    search_type = data["type"]
    search_type = type
    if search_type == "song":
        songs = search_songs_song(search_name)
    elif search_type == "artist":
        songs = search_songs_artist(search_name)
    elif search_type == "album":
        songs = search_songs_album(search_name)
    else:
        return "Invalid search type"
    return songs


@app.get('/all-songs/')
async def get_all_songs(user=Depends(manager)):
    songs = get_all_songs()
    return songs


@app.get('/all-playlists')
async def get_all_playlists(user=Depends(manager)):
    user_email = user
    playlists = get_all_playlists_db(user_email)
    return playlists


@app.post('/create-playlist/')
async def create_playlist(data: PlaylistData):
    data = data.dict()
    playlist_name = data["playlist_name"]
    songs = data["songs"]
    playlist_name = playlist_name.lower()
    user_email = "harsh13092001@gmail.com"
    check_playlist = check_playlist_name(playlist_name, user_email)
    if check_playlist == True:
        return "Playlist already exists"
    else:
        playlist_status = create_new_playlist(playlist_name, user_email, songs)
        return playlist_status


@app.post('/add-to-playlist/')
async def add_to_playlist(data: PlaylistData):
    data = data.dict()
    playlist_name = data["playlist_name"]
    songs = data["songs"]
    playlist_name = playlist_name.lower()
    user_email="harsh13092001@gmail.com"
    check_playlist = check_playlist_name(playlist_name, user_email)
    if check_playlist == False:
        return "Playlist doesn't exist"
    else:
        playlist_status = add_to_playlist_db( playlist_name, user_email, songs)
        return playlist_status
