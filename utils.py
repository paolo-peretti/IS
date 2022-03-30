from models import User, Listing
from extensions import db
import re
import random
from costants import *






def get_feature_value(request, feature):

    try:
        feature_value = request.form[feature]
        if 'on' in feature_value:
            return feature
        else:
            return ''
    except Exception:
        return ''



def get_listings(search_query):



    # search_query = [district, type_room, min, max, features]


    check_for_AND_sintax = False

    query = "SELECT * FROM listings "
    if search_query[0] != '': # district

        query += 'WHERE '
        query += "listings.district = '" + search_query[0] + "' "
        check_for_AND_sintax = True



    if search_query[2] != '': # Min Price

        if check_for_AND_sintax:
            query += "AND "
        else:
            query += 'WHERE '

        query += " listings.price >= '" + str(search_query[2]) + "' "
        check_for_AND_sintax = True

    if search_query[3] != '':  # Max Price

        if check_for_AND_sintax:
            query += "AND "
        else:
            query += 'WHERE '

        query += "listings.price <= '" + str(search_query[3]) + "' "

    query += "ORDER BY listings.price; "


    result_query = db.engine.execute(query)

    results = result_query.fetchall()

    listings_with_images = []

    if search_query[4] != [] or search_query[1] != '':  # features and types




        for result in results:

            if search_query[4] != [] :

                features = str(result[5])

                if ',' in features:
                    features = features.split(',')
                else:
                    features = [features]



                check_features = all(result in features for result in search_query[4])


            else:
                check_features = True



            if search_query[1] != '':

                types_available = str(result[3])


                types_available = types_available.split(',')



                check_types = search_query[1] in types_available
            else:
                check_types = True




            if check_features and check_types:
                # listings += [result]
                random_image_index = random.randrange(len(all_images))
                listings_with_images.append((result, all_images[random_image_index]))



    else:

        listings = results

        for listing in listings:
            random_image_index = random.randrange(len(all_images))
            listings_with_images.append((listing, all_images[random_image_index]))




    return listings_with_images




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
            password = decoding_password(found_user.password)
            if found_user.password != password:
                msg = 'This password is incorrect!'
        else:
            msg = 'This username is not found. Please check you have written it correctly.'

    return msg


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
    elements_to_update = []

    if username != '' and current_user.username != username:
        elements_to_update.append('username')
    if email != '' or current_user.email != email:
        elements_to_update.append('email')
    if name != '' or current_user.name != name:
        elements_to_update.append('name')
    if current_user.type_user != type_user:
        elements_to_update.append('type_user')


    if len(elements_to_update) > 0:


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



def add_user(info_user):

    username, email, password, password_confirm, name, type_user = info_user
    try:
        usr = User(username, email, password, name, type_user)
        db.session.add(usr)
        db.session.commit()
        return True
    except Exception:
        return False



def get_my_chats(current_user):

    query = 'SELECT "user1_ID", "user2_ID", message FROM public.messages WHERE messages."user1_ID"='
    query += "'" + str(current_user.id) + "'"
    query += 'or messages."user2_ID"='
    query += "'" + str(current_user.id) + "' "
    # query += 'ORDER BY messages."message_ID" DESC; '

    result_query = db.engine.execute(query)

    messages = result_query.fetchall()

    chats = {}
    interlocutors = {}

    for msg in messages:
        if str(msg[0]) != str(current_user.id):
            interlocutor_id = msg[0]
        else:
            interlocutor_id = msg[1]

        if interlocutor_id not in interlocutors.keys():

            query = "SELECT username FROM public.users WHERE id='"+str(interlocutor_id)+"'"
            result_query = db.engine.execute(query)
            interlocutor_name = result_query.fetchone()[0]

            interlocutors[interlocutor_id] = interlocutor_name
        else:
            interlocutor_name = interlocutors[interlocutor_id]

        chats.setdefault(interlocutor_name, []).append((int(msg[0]),int(msg[1]),msg[2]))




    return chats


