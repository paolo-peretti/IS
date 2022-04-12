
from cryptography.fernet import Fernet

from models import User, Listing, Like, Roommate
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


def get_my_listings(current_user):

    query = "SELECT * FROM listings "
    query += 'WHERE '
    query += "listings.owner_id = '" + str(current_user.id) + "' "

    result_query = db.engine.execute(query)
    listings = result_query.fetchall()

    listings_with_images = []

    for listing in listings:
        random_image_index = random.randrange(len(all_images))
        listings_with_images.append((listing, all_images[random_image_index]))


    return listings_with_images



def get_my_favorites(user_ID):

    listings = []

    try:
        query = 'SELECT "listing_ID" FROM likes '
        query += 'WHERE likes."user_ID" '
        query += "= " + str(user_ID) + " ;"

        result_query = db.engine.execute(query)
        results = result_query.fetchall()


        for listing in results:
            listings.append(int(listing[0]))


    except Exception:
        pass


    return listings






def add_like_to_listing(listing_id, user_id):

    try:
        like = Like(user_id, listing_id)
        db.session.add(like)
        db.session.commit()
        return True
    except Exception:
        return False

def add_roommate(user_id, listing_id):

    try:
        roommate = Roommate(user_id, listing_id)
        db.session.add(roommate)
        db.session.commit()
        return True
    except Exception:
        return False


def delete_like_to_listing(listing_id, user_id):

    try:

        query = "DELETE FROM likes "
        query += 'WHERE '
        query += 'likes."listing_ID" = '
        query += str(int(listing_id)) + " AND "
        query += 'likes."user_ID" = '
        query += str(int(user_id))


        db.engine.execute(query)
        db.session.commit()

        return True
    except Exception:
        return False




def delete_my_listings(listing_id):

    try:

        query = "DELETE FROM listings "
        query += 'WHERE '
        query += 'listings."house_ID" = '
        query += "'" + str(listing_id) + "' "

        db.engine.execute(query)
        db.session.commit()

        return True
    except Exception:
        return False




def delete_my_review(review_id):

    # print(review_id)

    try:

        query = "DELETE FROM reviews "
        query += 'WHERE '
        query += 'reviews."review_ID" = '
        query += "" + str(review_id) + " "

        db.engine.execute(query)
        db.session.commit()

        return True
    except Exception:
        return False






def add_a_listing(search_query, current_user_id):

    address, district, types_str, price, features_str = search_query

    try:
        listing = Listing(address, district, types_str, price, features_str, current_user_id)
        db.session.add(listing)
        db.session.commit()
        return True
    except Exception:
        return False


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



def update_a_listing(elements_to_update, listing_id):

    try:
        listing = Listing.query.filter_by(house_ID=int(listing_id)).first()


        if 'district' in list(elements_to_update.keys()):
            listing.district = elements_to_update['district']
        if 'types_str' in list(elements_to_update.keys()):
            listing.type_room = elements_to_update['types_str']
        if 'price' in list(elements_to_update.keys()):
            listing.price = elements_to_update['price']
        if 'features_str' in list(elements_to_update.keys()):
            listing.features = elements_to_update['features_str']

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




def get_reviews_of_listing(listing_ID):

    results = []

    try:
        query = 'SELECT users.username, reviews."user_ID", reviews.text, reviews.num_flag, reviews."review_ID" '
        query += 'FROM reviews INNER JOIN users ON reviews."user_ID" = users.id '
        query += 'WHERE reviews."listing_ID"'
        query += "= '" + str(listing_ID) + "' ;"

        result_query = db.engine.execute(query)
        results = result_query.fetchall()
        # print(results)

    except Exception:
        pass

    return results



def get_roommates_of_listing(listing_ID):

    results = []

    try:
        query = 'SELECT users.id, users.username, users.name, users.email, users.description, roommates.id '
        query += 'FROM roommates INNER JOIN users ON roommates."user_ID" = users.id '
        query += 'WHERE roommates."listing_ID"'
        query += "= '" + str(listing_ID) + "' ;"

        result_query = db.engine.execute(query)
        results = result_query.fetchall()
        # print(results)

    except Exception:
        pass

    return results


def delete_roommate_from_listing(roommate_id):

    try:
        query = "DELETE FROM roommates "
        query += 'WHERE '
        query += 'roommates.id = '
        query += "" + str(roommate_id) + " "

        db.engine.execute(query)
        db.session.commit()

        return True
    except Exception:
        return False