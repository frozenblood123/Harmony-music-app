import os
from dotenv import load_dotenv
from pymongo import MongoClient
from passlib.hash import sha256_crypt

load_dotenv()
mongo_uri = os.getenv("mongo_uri")
client = MongoClient(mongo_uri)
db = client.get_database("harmony_users")
profile = db.user_profile
profile_songs = db.all_songs


def check_user(email):
    result = profile.find_one({"email": email})
    if result == None:
        return False
    else:
        return True


def encrypt_password(pswd):
    enc_pswd = sha256_crypt.encrypt(pswd)
    return enc_pswd


def add_to_mongo(data, enc_pswd):
    data.pop("pswd")
    data.pop("cpswd")
    data.update(pswd=enc_pswd)
    profile.insert_one(data)


def get_password(email):
    info = profile.find_one({"email": email})
    stored_pswd = info["pswd"]
    return stored_pswd


def verify_password(entered_pswd, stored_pswd):
    verification = sha256_crypt.verify(entered_pswd, stored_pswd)
    return verification


def get_user_info(email):
    user_info = {}
    info = profile.find_one({"email": email})
    for i in info:
        if i != "_id" and i != "pswd":
            user_info[i] = info[i]
    return user_info


def search_songs_song(search_name):
    retrived_songs = []
    info = profile_songs.find({"_song": search_name})
    for i in info:
        i.pop("_id")
        retrived_songs.append(i)
    return retrived_songs

def search_songs_artist(search_name):
    retrived_songs = []
    info = profile_songs.find({"_artist": search_name})
    for i in info:
        i.pop("_id")
        retrived_songs.append(i)
    return retrived_songs

def search_songs_album(search_name):
    retrived_songs = []
    info = profile_songs.find({"_album": search_name})
    for i in info:
        i.pop("_id")
        retrived_songs.append(i)
    return retrived_songs

def get_all_songs():
    retrived_songs = []
    info = profile_songs.find()
    for i in info:
        i.pop("_id")
        retrived_songs.append(i)
    return retrived_songs

def check_playlist_name(playlist_name, user_email):
    user_profile = profile.find_one({"email": user_email})
    for i in user_profile["playlists"]['name']:
        if i == playlist_name:
            return True
        else:
            return False


def get_all_playlists_db(user_email):
    user_profile = profile.find_one({"email": user_email})
    retrived_playlists = user_profile["playlists"]
    return retrived_playlists


def create_new_playlist(playlist_name, user_email, songs=[]):
    try:
        user_profile = profile.find_one({"email": user_email})
        user_profile["playlists"]["name"].append(playlist_name)
        user_profile["playlists"]["playlist_songs"].update(
            {playlist_name: songs})
        profile.update_one({"email": user_email}, {"$set": user_profile})
        return "Playlist created successfully"
    except:
        return "Error creating playlist"


create_new_playlist("test", "harsh13092001@gmail.com")
