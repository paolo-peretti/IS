import ast

from cryptography.fernet import Fernet

from models import User, Listing
from costants import *
import re





def from_string_to_list(text):
    search_query = ast.literal_eval(text)

    return search_query


# it analizes the value of a check input
def get_feature_value(request, feature):

    try:
        feature_value = request.form[feature]
        if 'on' in feature_value:
            return feature
        else:
            return ''
    except Exception:
        return ''




# check for add a listing
def msg_adding_listing(search_query):

    address, district, types_str, price, features_str = search_query

    msg=''

    if address == '':
        msg = 'You have to specify an address!'
    elif district == '':
        msg = 'You have to specify a district!'
    elif types_str == '':
        msg = 'You have to choose the types of availability for the house!'
    else:
        try:
            if isinstance(int(price), int):
                msg = ''
        except Exception:
            msg = 'You have to put a valid value for the price!'

    return msg



def decoding_password(password):

    key_pass = 'NyaskKIJZz-Y0cIV0g38qB0UWi_1T7SuG3nTUfhrjbU='
    key_pass = key_pass.encode()

    password = password.encode()

    dencryption_pass = Fernet(key_pass)

    password = dencryption_pass.decrypt(password).decode()

    return password



def encoding_password(password):

    key_pass = 'NyaskKIJZz-Y0cIV0g38qB0UWi_1T7SuG3nTUfhrjbU='
    key_pass = key_pass.encode()


    encryption_type_pass = Fernet(key_pass)


    password = encryption_type_pass.encrypt(password.encode()).decode()

    return password


def check_email(email):
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.fullmatch(regex, email)



def check_auth(username, password):

    msg = ''
    if username == '':
        msg = 'Missing username.'
    elif password == '':
        msg = 'Missing password.'
    else:
        found_user = User.query.filter_by(username=username).first()
        if found_user:
            if decoding_password(found_user.password) != password:
                msg = 'This password is incorrect!'
        else:
            msg = 'This username is not found. Please check you have written it correctly.'

    return msg, found_user


def check_registration_info(info_user):

    username, email, password, password_confirm, name, type_user = info_user
    msg = ''
    if username == '':
        msg = 'Missing username.'
    elif password == '':
        msg = 'Missing password.'
    elif email == '':
        msg = 'Missing email.'
    elif name == '':
        msg = 'Missing name.'
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


def check_update_info(info_user, current_user):

    username, email, name, type_user = info_user
    msg = ''
    elements_to_update = {}


    if username != '' and current_user.username != username:
        elements_to_update['username'] = username
    if email != '' and current_user.email != email:
        elements_to_update['email'] = email
    if name != '' and current_user.name != name:
        elements_to_update['name'] = name
    if current_user.type_user != type_user:
        elements_to_update['type_user'] = type_user


    if len(list(elements_to_update.keys())) > 0:


        if check_email(email) == False:

            msg = 'This is not a valid email address. Please try again.'

        else:

            found_user = User.query.filter_by(username=username).first()

            if found_user:
                msg = 'This username already exists. Please choose another username.'
            else:
                found_user = User.query.filter_by(email=email).first()
                if found_user:
                    msg = 'This email is already in use.'

    else:

        msg = 'You have not changed anything. '

    return msg, elements_to_update





def check_update_listing(search_query, listing):

    address, district, types_str, price, features_str = search_query

    elements_to_update = {}


    if listing.district != district:
        elements_to_update['district'] = district
    if listing.type_room != types_str:
        elements_to_update['types_str'] = types_str
    if int(listing.price) != int(price):
        elements_to_update['price'] = int(price)
    if listing.features != features_str:
        elements_to_update['features_str'] = features_str


    return elements_to_update



def check_password_update(info_user, current_user):

    old_password, password, password_confirm = info_user

    msg = ''
    elements_to_update = {}

    if password != password_confirm:
        msg = 'The password does not match with the password confirmation!'
    elif password == '':
        msg = 'You have to write something to the password.'
    elif decoding_password(current_user.password) != old_password:
        msg = 'The old password you entered is incorrect.'
    else:
        elements_to_update['password'] = encoding_password(password)

    return msg, elements_to_update



# used to get some value as list and to get a boolean that shows if the listing is valid
def get_listing_info(listing_id):

    try:
        listing = Listing.query.filter_by(house_ID=int(listing_id)).first()

        types_available = listing.type_room.split(',')
        features = listing.features.split(',')

        try:
            if isinstance(int(listing.price), int):
                price = int(listing.price)
        except Exception:

            return False, [], listing

        listing_info = [listing.address, listing.district, types_available, price, features]

        return True, listing_info, listing

    except Exception:
        return False, [], listing



def get_image(result_id):
    if result_id < len(all_images)-1:
        return all_images[result_id]
    while True:
        result_id = int(result_id/len(all_images))
        if result_id < len(all_images)-1:
            return all_images[result_id]

