import items as items
from flask import render_template, request, session, flash, url_for, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from extensions import app, db
from utils import *
from models import User, Message, Listing

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



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

        # print(current_user.is_authenticated)

        # if "user" in session:
        #     user = session["user"]
        #     return render_template('index.html', usr=user, items=items, all_districts=all_districts)

        return render_template('index.html', items=items, all_districts=all_districts, user_favorites=user_favorites)


    else:

        # if "user" in session:
        #     user = session["user"]
        #     return render_template('index.html', usr=user, all_districts=all_districts)


        return render_template('index.html', all_districts=all_districts)


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

    return redirect(url_for('index'), code=307) #post


@app.route('/unlike/<listing_id>', methods=['GET'])
@login_required
def unlike(listing_id):


    if delete_like_to_listing(listing_id, current_user.id):
        flash('You have deleted this listing to your favorites listings!', 'info')
    else:
        flash('Something went wrong, please try again.', 'error')


    return redirect(url_for('index'), code=307) #post


@app.route('/my_favorites', methods=['POST', 'GET'])
@login_required
def my_favorites():

    if request.method == 'POST':
        pass
    else:

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
        session["messages"] = messages


        return render_template('chats.html', chats=messages, current_interlocutor=interlocutor, test_chats=True)


    else:

        test_chats = True

        if interlocutor == 'none':

            if "messages" in session:
                messages = session["messages"]
            else:
                messages = get_my_chats(current_user)
                session["messages"] = messages

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

            if "messages" in session:
                messages = session["messages"]
            else:
                messages = get_my_chats(current_user)
                session["messages"] = messages



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
    session.pop("messages", None)
    logout_user()
    return redirect(url_for("index"))








if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


