from models import User
from extensions import db
import re

def decoding_password(password):
    return password

def encoding_password(password):
    return password


def check_email(email):
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)


def check_auth(info_user):

    username, password = info_user
    msg = ''
    if username == '':
        msg = 'Missing username.'
    elif password == '':
        msg = 'Missing password.'
    else:
        found_user = User.query.filter_by(username=username).first()
        if found_user:
            password = decoding_password(password)
            if found_user.password != password:
                msg = 'This password is incorrect!'
        else:
            msg = 'This username is not found. Please check you have written it correctly.'

    return msg


def check_registration_info(info_user):

    username, email, password, password_confirm = info_user
    msg = ''
    if username == '':
        msg = 'Missing username.'
    elif password == '':
        msg = 'Missing password.'
    elif email == '':
        msg = 'Missing email.'
    elif password != password_confirm:
        msg = 'Password confirmation was unsuccessful.'
    elif check_email(email) == False:
        msg = 'This is not a valid email address. Please try again.'
    else:
        found_user = User.query.filter_by(username=username).first()
        if found_user:
            msg = 'This username already exists. Please choose another username.'
        else:
            found_user = User.query.filter_by(email=email).first()
            if found_user:
                msg = 'This email is already in use.'

    return msg


def add_user(info_user):

    username, email, password, password_confirm = info_user
    try:
        usr = User(username, email, password)
        db.session.add(usr)
        db.session.commit()
        return True
    except Exception:
        return False
