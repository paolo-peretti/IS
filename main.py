from flask import render_template, request, session, flash, url_for, redirect
from extensions import app, db
from models import User


@app.route('/')
def index():

    if "user" in session:
        user = session["user"]
        return render_template('index.html', usr=user)

    return render_template('index.html')





@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        session["user"] = username

        found_user = User.query.filter_by(username=username).first()

        if username == '' or password == '':
            flash('Missing username or password.', 'error')
            return render_template('login.html', type='signIn')

        if found_user:
            if found_user.password != password:
                flash('This password is incorrect!', 'error')
                return render_template('login.html', type='signIn')
        else:
            flash('This username is not found. Please check you have written it correctly.', 'error')
            return render_template('login.html', type='signIn')
            # usr = User(username, 'username', password)
            # db.session.add(usr)
            # db.session.commit()


        return redirect(url_for("index"))
    else:
        return render_template('login.html', type='signIn')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        session["user"] = username

        # found_user = User.query.filter_by(email=email).first()
        #
        # if found_user:
        #     flash('This email address is already registered.', 'info')
        #     return render_template('login.html')
        # else:
        #     usr = User(username, 'username', password)
        #     db.session.add(usr)
        #     db.session.commit()
        #
        # flash("You have been logged in.", "info")
        return redirect(url_for("index"))
    else:
        return render_template('login.html', type='signUp')


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


