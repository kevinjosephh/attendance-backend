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

    def courses(self):
        courses = self.classroom_repository.read_all()
        result = []
        for course in courses:
            data = {
                'id': str(course['_id']),
                'class': course['class'],
                'start_date': course['start_date'],
                'end_date': course['end_date'],
            }
            result.append(data)
        return result