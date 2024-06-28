

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
class DataBase:
    def __init__(self):
            mongo_path = os.getenv('MONGO_PATH')
            db_name = os.getenv("DB_NAME")
            self.client = MongoClient(mongo_path)
            self.db = self.client[db_name]
        