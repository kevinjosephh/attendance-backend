import json

from bson import json_util
from flask import Blueprint, jsonify, request, redirect

from src.attendance.attendance_bo import AttendanceBO
from src.students.students_bo import UsersBO

users_blueprint = Blueprint('users', __name__, url_prefix='/users/api/v1')

users_bo = UsersBO()
attendance_bo = AttendanceBO()

@users_blueprint.route('/ping')
def index():
    return jsonify({'status': 'Welcome to Students!'})


@users_blueprint.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    email = str(data['email']).strip()
    password = str(data['password']).strip()
    user = users_bo.login(email, password)
    return json_util.dumps(user)

@users_blueprint.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    first_name = str(data['firstName']).strip()
    last_name = str(data['lastName']).strip()
    role = str(data['role']).strip()
    roll_no = str(data['rollNo']).strip()
    class_name = str(data['className']).strip()
    email = str(data['email']).strip().lower()
    password = str(data['password']).strip()
    token = users_bo.register(email=email, password=password, first_name=first_name, last_name=last_name, role=role, roll_no=roll_no, class_name=class_name)
    return jsonify({'token': token})

@users_blueprint.route('/log', methods=['POST'])
def log():
    data = json.loads(request.data)
    id = str(data['id']).strip()
    return attendance_bo.log_attendance(id=id)

@users_blueprint.route('/log', methods=['POST'])
def get_log():
    data = json.loads(request.data)
    name = str(data['class_name']).strip()
    date = str(data['date']).strip()
    data = attendance_bo.fliter_class(name=name,date=date)
    return json_util.dumps(data)