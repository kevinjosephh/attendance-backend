import datetime

from src.constants import MONGO_CLIENT
from src.schema_constants import CUSTOMER_DB, CUSTOMER_DB_CLASSROOM


class ClassroomRepository:
    def __init__(self):
        self.schema = MONGO_CLIENT[CUSTOMER_DB][CUSTOMER_DB_CLASSROOM]

    def create(self, document):
        document['created_at'] = datetime.datetime.utcnow()
        document['updated_at'] = datetime.datetime.utcnow()
        return self.schema.insert_one(document=document)

    def read(self, document):
        return self.schema.find_one(filter=document)

    def read_all(self):
        return self.schema.find()