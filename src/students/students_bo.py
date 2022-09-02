import hashlib
import uuid

from src.students.students_repository import StudentsRepository


class UsersBO:
    def __init__(self):
        self.users_repository = StudentsRepository()

    def _read(self, document):
        user = self.users_repository.read(document=document)
        return user

    def login(self, email, password):
        user = self.users_repository.read({'email': email})
        if user is not None and not ('account' in user and user['account'] or 'deleted' in user and user['deleted']):
            salt = user["salt"]
            db_password = password + salt
            h = hashlib.md5(db_password.encode())
            if user['password'] == h.hexdigest():
                return user
            else:
                raise Exception('Invalid Credentials %s' % email)
        raise Exception('User %s does not exist.' % email)

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