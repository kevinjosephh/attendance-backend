from flask_httpauth import HTTPTokenAuth
from src.constants import JWT_SECRET_KEY
import jwt
import logging

auth = HTTPTokenAuth(scheme='Bearer')
logger = logging.getLogger("auth_bo")


@auth.verify_token
def verify_token(token):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
    except Exception as ex:
        logger.info(ex)
        return None


@auth.get_user_roles
def get_user_roles(user):
    try:
        return user['role']
    except Exception as ex:
        logger.info(ex)
        return None


