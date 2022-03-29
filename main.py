import ast

from flask import render_template, request, session, flash, url_for, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from extensions import app, db
from utils import *
from models import User, Message

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

        # print(current_user.is_authenticated)

        # if "user" in session:
        #     user = session["user"]
        #     return render_template('index.html', usr=user, items=items, all_districts=all_districts)

        return render_template('index.html', items=items, all_districts=all_districts)


    else:

        # if "user" in session:
        #     user = session["user"]
        #     return render_template('index.html', usr=user, all_districts=all_districts)


        return render_template('index.html', all_districts=all_districts)




@app.route('/send_message/<id_owner>', methods=['POST', 'GET'])
@login_required
def send_message(id_owner):
    # print(id_owner)

    if request.method == 'POST':
        # print('message')
        message = request.form["message"]
        if message != '':

            msg = Message(current_user.id, id_owner, message)
            db.session.add(msg)
            db.session.commit()

            flash('You sent the message successfully!', 'message')
            return redirect(url_for("index"))

        else:
            flash('You have to write something to send a message!', 'message')
            return render_template('send_message.html', id_owner=id_owner)

    else:

        return render_template('send_message.html', id_owner=id_owner)




@app.route('/update_user_informations', methods=['POST', 'GET'])
@login_required
def update_user_informations():
    # print(id_owner)

    if request.method == 'POST':
        pass

    else:

        pass

        # return redirect(url_for("login"))

@app.route('/chats/<interlocutor>', methods=['POST', 'GET'])
@login_required
def chats(interlocutor):

    if request.method == 'POST':

        print(interlocutor)
        message = request.form["message"]
        print(message)


        return render_template('chats.html', chats=['messages'], current_interlocutor=interlocutor)

    else:

        if interlocutor == 'none':

            messages = get_my_chats(current_user)
            session["messages"] = messages
            try:
                interlocutor = list(messages.keys())[0]
            except Exception:
                interlocutor = 'none'

        else:
            if "messages" in session:
                messages = session["messages"]
            else:
                session["messages"] = get_my_chats(current_user)



        return render_template('chats.html', chats=messages, current_interlocutor=interlocutor)



@app.route('/my_listings', methods=['POST', 'GET'])
@login_required
def my_listings():
    # print(id_owner)

    if request.method == 'POST':
        pass

    else:

        pass




@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':

        username = request.form["username"]
        password = request.form["password"]

        msg, user = check_auth([username, password])

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

        msg, user = check_registration_info(info_user)

        if msg == '':
            status = add_user(info_user)
            if status:
                # session["user"] = user

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


