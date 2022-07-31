import json
from flask import Blueprint, jsonify, request, redirect

from src.students.students_bo import UsersBO

users_blueprint = Blueprint('users', __name__, url_prefix='/users/api/v1')

users_bo = UsersBO()

@users_blueprint.route('/ping')
def index():
    return jsonify({'status': 'Welcome to Students!'})


@users_blueprint.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    email = str(data['email']).strip()
    password = str(data['password']).strip()
    user = users_bo.login(email, password)
    return jsonify(user)

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

