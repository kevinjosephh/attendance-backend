import datetime

import pymongo
from bson import ObjectId

from app.constants import MONGO_CLIENT
from app.schema_constants import CUSTOMER_DB, CUSTOMER_DB_ATTENDANCE


class AttendanceRepository:
    def __init__(self):
        self.schema = MONGO_CLIENT[CUSTOMER_DB][CUSTOMER_DB_ATTENDANCE]

    def create(self, document):
        document['created_at'] = datetime.datetime.utcnow()
        document['updated_at'] = datetime.datetime.utcnow()
        self.schema.insert_one(document=document)

    def read(self, document):
        return self.schema.find_one(filter=document)

    def read_all(self, document):
        return self.schema.find(filter=document)

if __name__ == '__main__':
    a= AttendanceRepository()
    date = '2022-09-01'
    date2= '2022-09-03'
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    date_obj1 = datetime.datetime.strptime(date2, '%Y-%m-%d')
    start_date = date_obj.replace(hour=0, minute=0, second=0)
    end_date = date_obj1.replace(hour=23, minute=59, second=59)
    print(start_date, end_date)
    today=datetime.datetime.today()
    print(a.read(document={'classroom': 'TYBSc', 'created_at': {'$gte': start_date, '$lte': today}}))
    # print(a.read())