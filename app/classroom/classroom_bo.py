import bson
from datetime import datetime

from app.students.students_bo import UsersBO

from app.classroom.classroom_repository import ClassroomRepository


class AttendanceBO:
    def __init__(self):
        self.users_bo = UsersBO()
        self.attendance_repository = ClassroomRepository()

    def add_class(self, id):
        pass