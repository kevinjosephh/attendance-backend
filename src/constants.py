import os
from pymongo import MongoClient


DB_URL = 'mongodb+srv://RDNATIONAL:rdnc@rdnc.p8phn.mongodb.net/test'

JWT_SECRET_KEY = "aGVsbG93b3JsZA=="

MONGO_CLIENT = MongoClient(DB_URL)

SCHEDULER_JOB = os.getenv('SCHEDULER_JOB', False)

ADMINS = ['josephkevin04@gmail.com']
