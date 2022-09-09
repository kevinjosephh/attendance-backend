from src.students.students_bo import UsersBO

from src.classroom.classroom_repository import ClassroomRepository


class ClassroomBO:
    def __init__(self):
        self.users_bo = UsersBO()
        self.classroom_repository = ClassroomRepository()

    def add_class(self, name, start_date, end_date):
        document = {
            'class': name,
            'start_date': start_date,
            'end_date': end_date,
        }
        return self.classroom_repository.create(document=document)