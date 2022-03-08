from models import User


def decoding_password(password):
    return password


def auth(info_user):

    username, password = info_user
    found_user = User.query.filter_by(username=username).first()
    msg = ''
    if username == '' or password == '':
        msg = 'Missing username or password.'
    else:
        if found_user:
            password = decoding_password(password)
            if found_user.password != password:
                msg = 'This password is incorrect!'
        else:
            msg = 'This username is not found. Please check you have written it correctly.'

    return msg