import os
from dotenv import load_dotenv
from pymongo import MongoClient
from passlib.hash import sha256_crypt

load_dotenv()
mongo_uri = os.getenv("mongo_uri")
client = MongoClient(mongo_uri)
db = client.get_database("harmony_users")
profile = db.user_profile


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
