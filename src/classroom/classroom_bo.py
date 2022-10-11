import datetime

from src.students.students_bo import UsersBO

from src.classroom.classroom_repository import ClassroomRepository


class ClassroomBO:
    def __init__(self):
        self.users_bo = UsersBO()
        self.classroom_repository = ClassroomRepository()

    def add_class(self, name, start_date, end_date):
        document = {
            'class': name,
            'start_date': datetime.datetime.strptime(start_date,'%d-%m-%y'),
            'end_date': datetime.datetime.strptime(end_date,'%d-%m-%y'),
        }
        return self.classroom_repository.create(document=document)

    def course(self,document):
        course = self.classroom_repository.read(document=document)
        data = {
            'id': str(course['_id']),
            '_class': course['class'],
            'start_date': datetime.datetime.strftime(course['start_date'],'%d-%m-%y'),
            'end_date': datetime.datetime.strftime(course['end_date'],'%d-%m-%y'),
        }
        return data
    def courses(self):
        courses = self.classroom_repository.read_all()
        result = []
        for course in courses:
            data = {
                'id': str(course['_id']),
                '_class': course['class'],
                'start_date': datetime.datetime.strftime(course['start_date'],'%d-%m-%y'),
                'end_date': datetime.datetime.strftime(course['end_date'],'%d-%m-%y'),
            }
            result.append(data)
        return result

if __name__ == '__main__':
    classroom = ClassroomBO()
    print(classroom.add_class('TYBSc','01-10-22','31-03-23'))