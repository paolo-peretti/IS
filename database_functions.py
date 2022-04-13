
from models import User, Listing, Like, Roommate
from extensions import db
from utils import *




def add_user(info_user):

    username, email, password, password_confirm, name, type_user = info_user
    try:
        usr = User(username, email, encoding_password(password), name, type_user, '')
        db.session.add(usr)
        db.session.commit()
        return True
    except Exception:
        return False



def update_user(elements_to_update, current_user):


    try:
        user = User.query.filter_by(id=current_user.id).first()


        if 'username' in list(elements_to_update.keys()):
            user.username = elements_to_update['username']
        if 'email' in list(elements_to_update.keys()):
            user.email = elements_to_update['email']
        if 'name' in list(elements_to_update.keys()):
            user.name = elements_to_update['name']
        if 'type_user' in list(elements_to_update.keys()):
            user.type_user = elements_to_update['type_user']

        if 'password' in list(elements_to_update.keys()):
            user.password = elements_to_update['password']

        if 'description' in list(elements_to_update.keys()):
            user.description = elements_to_update['description']

        db.session.commit()
        return True
    except Exception:
        return False

