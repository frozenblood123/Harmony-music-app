from dotenv import load_dotenv
from pymongo import MongoClient
import json
import os

load_dotenv()
mongo_uri = os.getenv("mongo_uri")
client = MongoClient(mongo_uri)
db = client.get_database("harmony_users")
profile = db.all_songs

def add_songs():
    with open('backend/all_songs.json') as json_file:
        songs_json = json.load(json_file)
        for songs in songs_json:
            result = profile.find_one({"_song": songs["_song"]})
            if result is None:
                profile.insert_one(songs)
            else:
                print("song already exists", result)

add_songs()