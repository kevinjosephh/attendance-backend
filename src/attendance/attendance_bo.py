import bson
from datetime import datetime, timedelta

from src.students.students_bo import UsersBO
from src.classroom.classroom_bo import ClassroomBO

from src.attendance.attendance_repository import AttendanceRepository


class AttendanceBO:
    def __init__(self):
        self.users_bo = UsersBO()
        self.classroom_bo = ClassroomBO()
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
        attends = self.attendance_repository.read_all(document={'user_id':id})
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

    def report(self, id):
        attends = self.attendance_repository.count_all(document={'user_id':id})
        user = self.users_bo.profile(id=id)
        course = self.classroom_bo.course(document={'class': user['class_name']})
        start_date = course['start_date']
        end_date = datetime.today()
        dt = start_date
        sunday_list=[]
        while dt < end_date:
            weekday = int(dt.strftime('%w'))
            if weekday==0:
                sunday_list.append(dt)
            dt += timedelta(days=1)
        total_days = (end_date-start_date).days
        absent = total_days+1-attends-len(sunday_list)
        data = {
            'start_date': datetime.strftime(start_date,'%d-%m-%y'),
            'end_date': datetime.strftime(end_date,'%d-%m-%y'),
            'days_present': str(attends),
            'days_absent': str(absent),
            'days_holiday': str(len(sunday_list)),
            'percentage':str((attends/absent)*100)
        }
        return data
    def fliter_class(self, name, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        start_date = date_obj.replace(hour=0, minute=0, second=0)
        end_date = date_obj.replace(hour=23, minute=59, second=59)
        return self.attendance_repository.read_all(document={'classroom': name, 'created_at': {'$gte':start_date,'$lte':end_date}})

if __name__ == '__main__':
    attends = AttendanceBO()
    print(attends.report('62e6c771c58ad4f71827b8d3'))