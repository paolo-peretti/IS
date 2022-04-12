
from flask import render_template, request, session, flash, url_for, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user


from extensions import app, db
from utils import *
from models import User, Message, Listing, Review

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/<search_query>')
@login_required
def back_to_search(search_query):

    search_query_splitted = search_query[1:-1].split(', ')
    search_query = []
    for val in search_query_splitted:
        print(val[-1])
        if val[-1] != ']':
            search_query.append(str(val[1:-1]))
        else:
            f = str(val[1:-1]).split(',')
            features = []
            print(f)
            for feature in f:
                print(feature)
                features.append(str(feature[1:-1]))


            search_query.append(features)

    print(search_query)


    items = get_listings(search_query)

    try:
        user_favorites = get_my_favorites(current_user.id)
    except Exception:
        # print('maybe the user is not logged in!')
        user_favorites = []

    return render_template('index.html', items=items, all_districts=all_districts, user_favorites=user_favorites,
                           search_query=search_query)


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':


        district = request.form["district"]



        min_price = request.form["min_price"]
        max_price = request.form["max_price"]



        if district not in all_districts:
            district=''

        # features
        features=[]
        try:
            bathroom = request.form["bathroom"] # private bathroom or shared bathroom
            features.append(bathroom)
        except Exception:
            bathroom=''
        try:
            furnished = request.form['furnished']
            if 'yes' in furnished:
                features.append('furnished')
        except Exception:
            furnished=''

        # features

        for feature in all_features_with_checkbox:
            value = get_feature_value(request, feature)
            if value != '':
                features.append(value)



        try:
            type_room = request.form['type_room']
        except Exception:
            type_room = ''




        search_query = [district, type_room, min_price, max_price, features]

        items = get_listings(search_query)

        try:
            user_favorites = get_my_favorites(current_user.id)
        except Exception:
            # print('maybe the user is not logged in!')
            user_favorites=[]

        return render_template('index.html', items=items, all_districts=all_districts, user_favorites=user_favorites, search_query=search_query)


    else:

        # if "user" in session:
        #     user = session["user"]
        #     return render_template('index.html', usr=user, all_districts=all_districts)


        return render_template('index.html', all_districts=all_districts, search_query=[])


@app.route('/like/<listing_id>', methods=['GET'])
@login_required
def like(listing_id):

    listings = get_my_favorites(current_user.id)

    if int(listing_id) not in listings:
        if add_like_to_listing(listing_id, current_user.id):
            flash('You have added this listing to your favorites listings!', 'info')
        else:
            flash('Something went wrong, please try again.', 'error')
    else:
        flash('Something went wrong, please try again.', 'error')

    return redirect(url_for('my_favorites'))


@app.route('/unlike/<listing_id>', methods=['GET'])
@login_required
def unlike(listing_id):


    if delete_like_to_listing(listing_id, current_user.id):
        flash('You have deleted this listing to your favorites listings!', 'info')
    else:
        flash('Something went wrong, please try again.', 'error')


    return redirect(url_for('my_favorites'))


@app.route('/my_favorites', methods=['GET'])
@login_required
def my_favorites():


    search_query = ['','','','',[]]

    items = get_listings(search_query)

    try:
        user_favorites = get_my_favorites(current_user.id)
    except Exception:
        # print('maybe the user is not logged in!')
        user_favorites = []

    favorite_listings = []
    for item in items:
        if int(item[0][0]) in user_favorites:
            favorite_listings.append(item)

    return render_template('my_favorites.html', items=favorite_listings, user_favorites=user_favorites)





@app.route('/write_review/<listing_id>', methods=['POST', 'GET'])
@login_required
def write_review(listing_id):

    if request.method == 'POST':

        review = request.form["review"]
        num_flag = request.form['num_flag']

        check_review = False

        try:
            if isinstance(int(num_flag), int):

                num_flag = int(num_flag)
                check_int=True

        except Exception:
            check_int=False

        if check_int:

            if review != '':

                listing = Listing.query.filter_by(house_ID=listing_id).first()

                if listing:
                    try:
                        review = Review(int(current_user.id), int(listing_id), review, int(num_flag))
                        db.session.add(review)
                        db.session.commit()

                        flash('The review is added successfully!', 'message')
                        check_review=True


                    except Exception:
                        flash('Something went wrong! Please try again later.', 'message')
                else:
                    flash('Something went wrong! Please try again later.', 'message')

            else:

                flash('You have to write something to send a message!', 'message')
        else:
            flash('You have to write a number for rating the listing!', 'message')

        if check_review:
            return redirect(url_for('my_favorites'))
        else:
            return render_template('write_review.html')
    else:
        return render_template('write_review.html')





@app.route('/read_reviews/<listing_id>/<search_query>', methods=['GET'])
@login_required
def read_reviews(listing_id, search_query):

    reviews = get_reviews_of_listing(int(listing_id))
    # reviews[0] = users.username, reviews."user_ID", reviews.text, reviews.num_flag, reviews.review_ID

    return render_template('read_reviews.html', items=reviews, search_query=search_query)





@app.route('/delete_review/<review_id>', methods=['GET'])
@login_required
def delete_review(review_id):


    review = Review.query.filter_by(review_ID=int(review_id)).first()

    if int(review.user_ID) == current_user.id:

        if delete_my_review(int(review_id)):
            flash('You have deleted the review successfully.', 'info')
        else:
            flash('Something went wrong, please try again.', 'error')
    else:
        flash('Something went wrong, please try again.', 'error')

    return redirect(url_for('my_favorites'))









@app.route('/update_user_informations', methods=['POST', 'GET'])
@login_required
def update_user_informations():

    if request.method == 'POST':


        try:

            username = request.form["username"]
            email = request.form["email"]
            name = request.form["name"]

            try:
                type_user = request.form['type_user']
            except Exception:
                print('something went wrong')
                type_user = 'searcher'

            check_info = True

        except Exception:

            check_info = False



        try:

            old_password = request.form["old_password"]
            password = request.form["password"]
            password_confirm = request.form["confirm_password"]

            check_pass = True

        except Exception:

            check_pass = False


        try:

            description = request.form["description"]
            # print(description)

            check_description = True

        except Exception:

            check_description = False


        if check_info:


            info_user = [username, email, name, type_user]

            msg, elements_to_update = check_update_info(info_user, current_user)

            if msg == '':

                status = update_user(elements_to_update, current_user)

                if status:
                    flash('You have update your informations successfully!', 'info')
                else:
                    flash('Something went wrong, please try again.', 'error')

            else:

                flash(msg, 'message')


            return render_template('login.html', type='update')


        if check_pass:

            info_user = [old_password, password, password_confirm]

            msg, elements_to_update = check_password_update(info_user, current_user)

            if msg == '':

                status = update_user(elements_to_update, current_user)

                if status:

                    flash('You have update your password successfully!', 'info')

                else:

                    flash('Something went wrong, please try again.', 'error')

            else:

                flash(msg, 'message')


            return render_template('login.html', type='update')


        if check_description:


            if description != '':

                if description != current_user.description:

                    elements_to_update = {}
                    elements_to_update['description'] = description

                    status = update_user(elements_to_update, current_user)

                    if status:

                        flash('You have set a description successfully!', 'info')

                    else:

                        flash('Something went wrong, please try again.', 'error')
                else:
                    flash('You have not changed anything, please try again.', 'error')
            else:
                flash('You have to write something here!', 'error')


            return render_template('login.html', type='update')

        flash('Something went wrong, please try again.', 'error')
        return render_template('login.html', type='update')



    else:

        return render_template('login.html', type='update')




@app.route('/chats/<interlocutor>', methods=['POST', 'GET'])
@login_required
def chats(interlocutor):

    if request.method == 'POST':


        message = request.form["message"]
        interlocutor = request.form["interlocutor"]


        if message != '':

            owner = User.query.filter_by(username=interlocutor).first()

            if owner:
                try:
                    msg = Message(current_user.id, owner.id, message)
                    db.session.add(msg)
                    db.session.commit()


                except Exception:
                    flash('Something went wrong! Please try again later.', 'message')
            else:
                flash('Something went wrong! Please try again later.', 'message')

        else:

            flash('You have to write something to send a message!', 'message')


        messages = get_my_chats(current_user)
        # session["messages"] = messages


        return render_template('chats.html', chats=messages, current_interlocutor=interlocutor, test_chats=True)


    else:

        test_chats = True

        if interlocutor == 'none':


            messages = get_my_chats(current_user)


            try:
                interlocutor = list(messages.keys())[0]
            except Exception:
                test_chats=False


        else:

            try:
                if isinstance(int(interlocutor), int):

                    id_owner = int(interlocutor)
                    owner = User.query.filter_by(id=id_owner).first()
                    if owner:
                        interlocutor = owner.username

            except Exception:
                pass



            messages = get_my_chats(current_user)




        return render_template('chats.html', chats=messages, current_interlocutor=interlocutor, test_chats=test_chats)



@app.route('/my_listings', methods=['GET'])
@login_required
def my_listings():

    listings = get_my_listings(current_user)
    return render_template('my_listings.html', items=listings)






@app.route('/delete_listings/<listing_id>')
@login_required
def delete_listings(listing_id):

    if delete_my_listings(listing_id):
        flash('This listing is deleted successfully!', 'info')
    else:
        flash('Something went wrong, please try again.', 'error')


    listings = get_my_listings(current_user)

    return render_template('my_listings.html', items=listings)


@app.route('/add_listing', methods=['POST', 'GET'])
@login_required
def add_listing():

    if request.method == 'POST':



        address = request.form["address"]

        district = request.form["district"]

        price = request.form["price"]


        if district not in all_districts:
            district = ''

        # features
        features = []
        try:
            bathroom = request.form["bathroom"]  # private bathroom or shared bathroom
            features.append(bathroom)
        except Exception:
            flash('You have to choose the type of bathroom !', 'message')
            return render_template('add_listing.html', all_districts=all_districts, type='add')
        try:
            furnished = request.form['furnished']
            if 'yes' in furnished:
                features.append('furnished')
        except Exception:
            flash('You have to choose if the house is furnished or not !', 'message')
            return render_template('add_listing.html', all_districts=all_districts, type='add')




        # features

        for feature in all_features_with_checkbox:
            value = get_feature_value(request, feature)
            if value != '':
                features.append(value)


        # type_room

        types = []

        for type_room in room_types:
            value = get_feature_value(request, type_room)
            if value != '':
                types.append(value)



        try:
            types_str = ','.join(types)
        except Exception:
            types_str = ''
        try:
            features_str = ','.join(features)
        except Exception:
            features_str = ''



        search_query = [address, district, types_str, price, features_str]



        msg = msg_adding_listing(search_query)



        if msg == '':

            if add_a_listing(search_query, current_user.id):
                flash('The listing is added successfully!', 'info')

                listings = get_my_listings(current_user)
                return render_template('my_listings.html', items=listings)

            else:
                flash('Something went wrong, please try again.', 'error')
                return render_template('add_listing.html', all_districts=all_districts, type='add')
        else:

            flash(msg, 'message')
            return render_template('add_listing.html', all_districts=all_districts, type='add')




    else:


        return render_template('add_listing.html', all_districts=all_districts, type='add')



@app.route('/update_listing/<listing_id>', methods=['POST', 'GET'])
@login_required
def update_listing(listing_id):


    check_listing_db, listing_info, listing = get_listing_info(listing_id)

    if check_listing_db:

        if request.method == 'POST':



            district = request.form["district"]

            price = request.form["price"]

            if district not in all_districts:
                district = ''

            # features
            features = []
            try:
                bathroom = request.form["bathroom"]  # private bathroom or shared bathroom
                features.append(bathroom)
            except Exception:
                flash('You have to choose the type of bathroom !', 'message')
                return render_template('add_listing.html', all_districts=all_districts, type='update', listing_info=listing_info)
            try:
                furnished = request.form['furnished']
                if 'yes' in furnished:
                    features.append('furnished')
            except Exception:
                flash('You have to choose if the house is furnished or not !', 'message')
                return render_template('add_listing.html', all_districts=all_districts, type='update', listing_info=listing_info)

            # features

            for feature in all_features_with_checkbox:
                value = get_feature_value(request, feature)
                if value != '':
                    features.append(value)

            # type_room

            types = []

            for type_room in room_types:
                value = get_feature_value(request, type_room)
                if value != '':
                    types.append(value)

            try:
                types_str = ','.join(types)
            except Exception:
                types_str = ''
            try:
                features_str = ','.join(features)
            except Exception:
                features_str = ''

            search_query = ['address', district, types_str, price, features_str]

            msg = msg_adding_listing(search_query)



            if msg == '':

                elements_to_update = check_update_listing(search_query, listing)


                if len(list(elements_to_update.keys())) > 0:

                    if update_a_listing(elements_to_update, int(listing_id)):

                        flash('The listing is updated successfully!', 'info')

                        listings = get_my_listings(current_user)
                        return render_template('my_listings.html', items=listings)

                    else:
                        flash('Something went wrong, please try again.', 'error')
                        return render_template('add_listing.html', all_districts=all_districts, type='update', listing_info=listing_info)

                else:
                    flash('You have not changed anything. ', 'error')
                    return render_template('add_listing.html', all_districts=all_districts, type='update', listing_info=listing_info)

            else:

                flash(msg, 'message')
                return render_template('add_listing.html', all_districts=all_districts, type='update', listing_info=listing_info)

        else: # GET
            return render_template('add_listing.html', all_districts=all_districts, type='update', listing_info=listing_info)




    else:
        flash('Something went wrong, please try again.', 'error')
        return render_template('base.html')




@app.route('/view_roommates/<listing_id>', methods=['POST', 'GET'])
@login_required
def view_roommates(listing_id):

    check_listing_db, listing_info, listing = get_listing_info(listing_id)

    if check_listing_db:

        if request.method == 'POST':

            username = request.form["username"]

            if username == '':
                msg = 'Missing username.'
                flash(msg, 'message')
            else:
                found_user = User.query.filter_by(username=username).first()

                if found_user:

                    status = add_roommate(found_user.id, listing_id)

                    if status:
                        msg = 'You have added successfully the user as roommate!'
                        flash(msg, 'message')
                    else:
                        msg = 'Something went wrong, please try again.'
                        flash(msg, 'message')

                else:
                    msg = 'This username is not found. Please check you have written it correctly.'
                    flash(msg, 'message')

            roommates = get_roommates_of_listing(listing_id)
            return render_template('view_roommates.html', items=roommates, listing=listing)


        else:

            roommates = get_roommates_of_listing(listing_id)
            # print(roommates)
            # users.id, users.username, users.name, users.email, users.description, roommates.id

            return render_template('view_roommates.html', items=roommates, listing=listing)


    else:
        flash('Something went wrong, please try again.', 'error')
        return render_template('base.html')



@app.route('/delete_roommate/<roommate_id>')
@login_required
def delete_roommate(roommate_id):

    found_roommate = Roommate.query.filter_by(id=roommate_id).first()

    if found_roommate:
        listing_id=found_roommate.listing_ID
        if delete_roommate_from_listing(roommate_id):
            flash('This roommate is deleted successfully!', 'info')
        else:
            flash('Something went wrong, please try again.', 'error')

        return redirect(url_for("view_roommates", listing_id=listing_id))
    else:
        flash('Something went wrong, please try again.', 'error')
        return render_template('base.html')








@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]

        msg, user = check_auth(username, password)

        if msg == '':
            # session["user"] = username

            login_user(user)


            return redirect(url_for("index"))
        else:
            flash(msg, 'message')
            return render_template('login.html', type='signIn')
    else:
        return render_template('login.html', type='signIn')



@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':

        username = request.form["username"]
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        password_confirm = request.form["confirm_password"]

        try:
            type_user = request.form['type_user']
        except Exception:
            print('something went wrong')
            type_user='searcher'

        info_user = [username, email, password, password_confirm, name, type_user]

        msg = check_registration_info(info_user)

        if msg == '':
            status = add_user(info_user)
            if status:


                flash('Welcome! You have registered successfully!', 'info')

                # sending a 307 status code instead of 302 should tell the browser to preserve the used HTTP method
                # and thus have the behaviour you're expecting. Your call to redirect would then look like this:

                return redirect(url_for('login'), code=307)
                # return redirect(url_for("index"))
            else:
                flash('Something went wrong, please try again.', 'error')
                return render_template('login.html', type='signUp')
        else:
            flash(msg, 'message')
            return render_template('login.html', type='signUp')
    else:
        return render_template('login.html', type='signUp')







@app.route('/logout')
@login_required
def logout():
    # print(current_user)
    logout_user()
    return redirect(url_for("index"))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500






if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


