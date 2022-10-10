import bson
from datetime import datetime

from src.students.students_bo import UsersBO

from src.attendance.attendance_repository import AttendanceRepository


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
        attendance = self.attendance_repository.read(document={'user_id': id})
        today = datetime.today()
        if attendance is None or (attendance['created_at']).strftime('%Y-%m-%d') != today.strftime('%Y-%m-%d'):
            self.attendance_repository.create(document=document)
            return True
        else:
            return False

    def all_log(self, id):
        attends = AttendanceRepository.read_all(document={'user_id':id})
        results = []
        for attend in attends:
            data = {
                'id': str(attend['_id']),
                'user_id': attend['id'],
                'classroom': attend['class_name'],
                'email': attend['email'],
                'roll_no': attend['roll_no']
            }
            results.append(data)
        return results
    def fliter_class(self, name, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        start_date = date_obj.replace(hour=0, minute=0, second=0)
        end_date = date_obj.replace(hour=23, minute=59, second=59)
        return self.attendance_repository.read_all(document={'classroom': name, 'created_at': {'$gte':start_date,'$lte':end_date}})