from flask import render_template, request, session, flash, url_for, redirect
from extensions import app, db

from utils import auth


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

        msg = auth([username, password])

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


