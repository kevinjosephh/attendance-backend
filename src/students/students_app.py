import json

from bson import json_util
from flask import Blueprint, jsonify, request

from src.classroom.classroom_bo import ClassroomBO
from src.attendance.attendance_bo import AttendanceBO
from src.students.students_bo import UsersBO

users_blueprint = Blueprint('users', __name__, url_prefix='/users/api/v1')

users_bo = UsersBO()
attendance_bo = AttendanceBO()
classroom_bo = ClassroomBO()

@users_blueprint.route('/ping')
def index():
    return jsonify({'status': 'Welcome to Students!'})


@users_blueprint.route('/login/', methods=['POST'])
def login():
    data = json.loads(request.data)
    email = str(data['email']).strip()
    password = str(data['password']).strip()
    user = users_bo.login(email, password)
    return json_util.dumps(user)

@users_blueprint.route('/student_register', methods=['POST'])
def register():
    data = json.loads(request.data)
    first_name = str(data['firstName']).strip()
    last_name = str(data['lastName']).strip()
    role = 'Student'
    roll_no = str(data['rollNo']).strip()
    class_name = str(data['className']).strip()
    email = str(data['email']).strip().lower()
    password = str(data['password']).strip()
    token = users_bo.register(email=email, password=password, first_name=first_name, last_name=last_name, role=role, roll_no=roll_no, class_name=class_name)
    return json_util.dumps(token)

@users_blueprint.route('/teacher_register', methods=['POST'])
def teacher_register():
    data = json.loads(request.data)
    first_name = str(data['firstName']).strip()
    last_name = str(data['lastName']).strip()
    role = 'Teacher'
    roll_no = str(data['rollNo']).strip()
    class_name = str(data['className']).strip()
    email = str(data['email']).strip().lower()
    password = str(data['password']).strip()
    token = users_bo.register(email=email, password=password, first_name=first_name, last_name=last_name, role=role, roll_no=roll_no, class_name=class_name)
    return json_util.dumps(token)

@users_blueprint.route('/profile/<id>/', methods=['GET'])
def profile(id):
    profile = users_bo.profile(id)
    return json_util.dumps(profile)

@users_blueprint.route('/student_profiles/', methods=['GET'])
def student_profiles():
    profile = users_bo.studentprofiles()
    return json_util.dumps(profile)

@users_blueprint.route('/teacher_profiles/', methods=['GET'])
def teacher_profiles():
    profile = users_bo.teacherprofiles()
    return json_util.dumps(profile)

@users_blueprint.route('/courses/', methods=['GET'])
def courses():
    courses = classroom_bo.courses()
    return json_util.dumps(courses)
@users_blueprint.route('/attendance/<id>/', methods=['GET'])
def view_attendance(id):
    profile = attendance_bo.all_log(id=id)
    return json_util.dumps(profile)

@users_blueprint.route('/log', methods=['POST'])
def log():
    data = json.loads(request.data)
    id = str(data['id']).strip()
    return jsonify(attendance_bo.log_attendance(id=id))

@users_blueprint.route('/student_log/', methods=['POST'])
def get_log():
    data = json.loads(request.data)
    name = str(data['class_name']).strip()
    date = str(data['date']).strip()
    data = attendance_bo.fliter_class(name=name,date=date)
    return jsonify(data)

@users_blueprint.route('/add_class/', methods=['POST'])
def add_class():
    data = json.loads(request.data)
    name = str(data['name']).strip()
    start_date = str(data['start_date']).strip()
    end_date = str(data['end_date']).strip()
    data = classroom_bo.add_class(name, start_date, end_date)
    return jsonify(data)