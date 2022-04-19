from models import Message, Like, Roommate, Review
from utils import *

from extensions import db
# This file contains many functions that modify the database

# USER

def add_user(info_user):

    username, email, password, password_confirm, name, type_user = info_user
    try:
        usr = User(username, email, encoding_password(password), name, type_user, '') # the last position is the description of the user
        db.session.add(usr) # adding this instance of User
        db.session.commit() # confirm the changes on the database
        return True
    except Exception:
        return False


def update_user(elements_to_update, current_user):


    try:
        user = User.query.filter_by(id=current_user.id).first()

        # we are updating the informations of the user instance in order to confirm the changes later
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


# ------------------------------------------------------------------------------------
# LISTING


def add_a_listing(search_query, current_user_id):

    address, district, types_str, price, features_str = search_query

    try:
        listing = Listing(address, district, types_str, price, features_str, current_user_id)
        db.session.add(listing)
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


                # this is a check for the features the user is searching for.
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
                img = get_image(result[0])

                listings_with_images.append((result, img))



    else:

        listings = results

        for listing in listings:
            img = get_image(listing[0])

            listings_with_images.append((listing, img))




    return listings_with_images


# for the renter, get all listings the renter owns
def get_my_listings(current_user):

    query = "SELECT * FROM listings "
    query += 'WHERE '
    query += "listings.owner_id = '" + str(current_user.id) + "' "

    result_query = db.engine.execute(query)
    listings = result_query.fetchall() # get all the results of the query

    listings_with_images = []

    for listing in listings:
        img = get_image(listing[0])
        listings_with_images.append((listing, img))


    return listings_with_images


# ------------------------------------------------------------------------------------
# LIKE

def add_like_to_listing(listing_id, user_id):

    try:
        like = Like(user_id, listing_id)
        db.session.add(like)
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


# ------------------------------------------------------------------------------------
# CHAT

def add_message(current_user, owner, message):

    try:
        msg = Message(current_user.id, owner.id, message)
        db.session.add(msg)
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

        # adding a key to the dictionary and a list of 1 value, or adding the value to the list related to the key
        chats.setdefault(interlocutor_name, []).append((int(msg[0]),int(msg[1]),msg[2]))




    return chats



# ------------------------------------------------------------------------------------
# REVIEW

def add_review(current_user, listing_id, review, num_flag):

    try:
        review = Review(int(current_user.id), int(listing_id), review, int(num_flag))
        db.session.add(review)
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


def get_reviews_of_listing(listing_ID):

    results = []

    try:
        query = 'SELECT users.username, reviews."user_ID", reviews.text, reviews.num_flag, reviews."review_ID" '
        query += 'FROM reviews INNER JOIN users ON reviews."user_ID" = users.id ' # using the inner join we'll work on 2 tables
        query += 'WHERE reviews."listing_ID"'
        query += "= '" + str(listing_ID) + "' ;"

        result_query = db.engine.execute(query)
        results = result_query.fetchall()
        # print(results)

    except Exception:
        pass

    return results


# ------------------------------------------------------------------------------------
# ROOMMATE


def add_roommate(user_id, listing_id):

    try:
        roommate = Roommate(user_id, listing_id)
        db.session.add(roommate)
        db.session.commit()
        return True
    except Exception:
        return False



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

