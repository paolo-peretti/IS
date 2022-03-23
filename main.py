from flask import render_template, request, session, flash, url_for, redirect
from extensions import app, db
from utils import *


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':


        district = request.form["district"]
        num_rooms = request.form["num_rooms"]
        min_price = request.form["min_price"]
        max_price = request.form["max_price"]



        # features
        features=[]
        try:
            bed = request.form["bed"]
            if 'on' in bed:
                features.append('bed')
        except Exception:
            pass
        try:
            bathroom = request.form["bathroom"]
            if 'on' in bathroom:
                features.append('bathroom')
        except Exception:
            pass





        search_query = [district, num_rooms, min_price, max_price, features]
        items = get_listings(search_query)

        if "user" in session:
            user = session["user"]
            return render_template('index.html', usr=user, items=items)

        return render_template('index.html', items=items)


    else:

        if "user" in session:
            user = session["user"]
            return render_template('index.html', usr=user)


        return render_template('index.html')


@app.route('/search')
def search():

    search_query = [None, 1, None, None, ['bed']]
    listings = get_listings(search_query)

    if "user" in session:
        user = session["user"]
        return render_template('index.html', usr=user)



    return render_template('index.html')


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





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


