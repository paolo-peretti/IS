from models import User, Listing
from extensions import db
import re



def get_listings(search_query):

    # search_query = [distrect, num_room, min, max, features]

    check_for_AND_sintax = False

    query = "SELECT * FROM listings WHERE "
    if search_query[0] != None: # distrect
        query += "listings.distrect = '" + search_query[0] +"' "
        check_for_AND_sintax = True
    if search_query[1] != None: # Num rooms
        if check_for_AND_sintax:
            query += "AND "
        query += "listings.num_room >= '"+ str(search_query[1]) + "' "
        check_for_AND_sintax = True
    if search_query[2] != None: # Min Price
        if check_for_AND_sintax:
            query += "AND "
        query += " listings.price >= '" + str(search_query[2]) + "' "
        check_for_AND_sintax = True
    if search_query[3] != None:  # Max Price
        if check_for_AND_sintax:
            query += "AND "
        query += "listings.price <= '" + str(search_query[3]) + "' "
    query += "ORDER BY listings.price; "


    result_query = db.engine.execute(query)

    results = result_query.fetchall()

    if search_query[4] != None:  # features
        listings = []
        for result in results:
            features = str(result[len(result) - 1])
            if ',' in features:
                features = features.split(',')
            else:
                features = [features]

            features_founded = 0
            for feature in features:
                if feature in search_query[4]:
                    features_founded += 1

            if features_founded == len(search_query[4]):
                listings += [result]



    return listings


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
