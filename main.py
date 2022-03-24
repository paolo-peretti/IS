from functools import wraps

from flask import render_template, request, session, flash, url_for, redirect
from flask_login import login_required, LoginManager, logout_user, login_user

from extensions import app, db
from utils import *







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

        if "user" in session:
            user = session["user"]
            return render_template('index.html', usr=user, items=items, all_districts=all_districts)

        return render_template('index.html', items=items, all_districts=all_districts)


    else:

        if "user" in session:
            user = session["user"]
            return render_template('index.html', usr=user, all_districts=all_districts)


        return render_template('index.html', all_districts=all_districts)




@app.route('/send_message/<id_owner>', methods=['POST', 'GET'])
def send_message(id_owner):

    if request.method == 'POST':
        pass

    else:

        print(id_owner)

        if "user" in session:
            user = session["user"]
            return render_template('send_message.html', usr=user)

        return redirect(url_for("login"))






@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        msg = check_auth([username, password])

        if msg == '':
            session["user"] = username

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
        password = request.form["password"]
        password_confirm = request.form["confirm_password"]

        info_user = [username, email, password, password_confirm]

        msg = check_registration_info(info_user)

        if msg == '':
            status = add_user(info_user)
            if status:
                session["user"] = username

                flash('Welcome! You have registered successfully!', 'info')
                return redirect(url_for("index"))
            else:
                flash('Something went wrong, please try again.', 'error')
                return render_template('login.html', type='signUp')
        else:
            flash(msg, 'message')
            return render_template('login.html', type='signUp')
    else:
        return render_template('login.html', type='signUp')







@app.route('/logout')
def logout():
    session.pop("user", None)
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


