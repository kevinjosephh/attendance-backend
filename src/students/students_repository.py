import datetime

import pymongo
from bson import ObjectId

from src.constants import MONGO_CLIENT
from src.schema_constants import CUSTOMER_DB, CUSTOMER_DB_USERS


class StudentsRepository:
    def __init__(self):
        self.schema = MONGO_CLIENT[CUSTOMER_DB][CUSTOMER_DB_USERS]

    def create(self, document):
        document['created_at'] = datetime.datetime.utcnow()
        document['updated_at'] = datetime.datetime.utcnow()
        self.schema.insert_one(document=document)

    def read(self, email):
        return self.schema.find_one(filter={'email': email})

    def read_by_id(self, id):
        return self.schema.find_one(filter={'_id': ObjectId(id)})