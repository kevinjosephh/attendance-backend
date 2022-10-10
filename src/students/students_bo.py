import datetime
import hashlib
import uuid

import bson
import jwt

from src.constants import JWT_SECRET_KEY
from src.students.students_repository import StudentsRepository


class UsersBO:
    def __init__(self):
        self.users_repository = StudentsRepository()

    def _read(self, document):
        user = self.users_repository.read(document=document)
        return user

    def get_token(self, user):
        obj = {
            'id': str(user['_id']),
            'name': user['name'] if 'name' in user else 'Creator',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'role': user['role'] if 'role' in user else 'USER',
            'permissions': user['permissions'] if 'permissions' in user else [],
            'session': str(uuid.uuid4())
        }
        return jwt.encode(obj, JWT_SECRET_KEY).decode('UTF_8')
    def login(self, email, password):
        user = self.users_repository.read({'email': email})
        if user is not None and not ('account' in user and user['account'] or 'deleted' in user and user['deleted']):
            salt = user["salt"]
            db_password = password + salt
            h = hashlib.md5(db_password.encode())
            if user['password'] == h.hexdigest():
                return self.profile(user['_id'])
            else:
                return 'Invalid Credentials %s' % email
        return 'User %s does not exist.' % email

    def register(self, email, password, first_name, last_name, role, roll_no, class_name):
        salt = str(uuid.uuid4())
        db_password = password + salt
        hashed = hashlib.md5(db_password.encode())
        document = {
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            'roll_no': roll_no,
            'class_name': class_name,
            'email': email,
            'password': hashed.hexdigest(),
            'salt': salt,
        }
        user = self._read(document={'email': email})
        if user is None:
            print('yes')
            self.users_repository.create(document)
            # TODO send email with the reset link.
            return self._read(document={'email': email})
        raise Exception('User %s already exist' % email)

    def profile(self, id):
        user = self._read(document={'_id':bson.ObjectId(id)})
        data = {
            'id': str(user['_id']),
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'role': user['role'],
            'roll_no': user['roll_no'],
            'class_name': user['class_name'],
            'email': user['email'],
            'password': user['password']
        }
        return data

    def studentprofiles(self):
        users = self.users_repository.read_all(document={
            'role':'Student'
        })
        result = []
        for user in users:
            data = {
                'id': str(user['_id']),
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'role': user['role'],
                'roll_no': user['roll_no'],
                'class_name': user['class_name'],
                'email': user['email'],
                'password': user['password']
            }
            result.append(data)
        return result

    def teacherprofiles(self):
        users = self.users_repository.read_all(document={
            'role':'Teacher'
        })
        result = []
        for user in users:
            data = {
                'id': str(user['_id']),
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'role': user['role'],
                'roll_no': user['roll_no'],
                'class_name': user['class_name'],
                'email': user['email'],
                'password': user['password']
            }
            result.append(data)
        return result

if __name__ == '__main__':
    user = UsersBO()
    print(user.profiles())