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
    info = profile.find_one({"email": email})
    return info


def search_songs_song(search_name):
    retrived_songs=[]
    info = profile_songs.find({"_song": search_name})
    for i in info:
        retrived_songs.append(i)
    return retrived_songs
    #return info

print(search_songs_song("Date"))