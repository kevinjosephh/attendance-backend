import bson
from datetime import datetime

from app.students.students_bo import UsersBO

from app.attendance.attendance_repository import AttendanceRepository


class AttendanceBO:
    def __init__(self):
        self.users_bo = UsersBO()
        self.attendance_repository = AttendanceRepository()

    def log_attendance(self, id):
        user = self.users_bo._read(document={'_id': bson.ObjectId(id)})
        document = {
            'user_id': id,
            'classroom': user['class_name'],
            'email': user['email'],
            'roll_no': user['roll_no']
        }
        attendance = self.attendance_repository.read(document={'_id': bson.ObjectId(id)})
        today = datetime.today()
        if attendance is None or (attendance['created_at']).strftime('%Y-%m-%d') != today.strftime('%Y-%m-%d'):
            self.attendance_repository.create(document=document)
            return '%s Successful' % user['roll_no']
        else:
            return '%s has been already marked' % user['roll_no']

    def fliter_class(self, name, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        start_date = date_obj.replace(hour=0, minute=0, second=0)
        end_date = date_obj.replace(hour=23, minute=59, second=59)
        return self.attendance_repository.read_all(document={'classroom': name, 'created_at': {'$gte':start_date,'$lte':end_date}})