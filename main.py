from flask import render_template, request, session, flash, url_for, redirect
from extensions import app, db
from models import User


@app.route('/')
def index():

    if "user" in session:
        user = session["user"]
        return render_template('index.html', usr=user)
    else:
        return render_template('index.html', usr=None)





@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        session["user"] = username

        found_user = User.query.filter_by(username=username).first()

        if found_user:
            flash('pass is : '+found_user.password,'info')
        else:
            usr = User(username, 'username', password)
            db.session.add(usr)
            db.session.commit()

        flash("You have been logged in.", "info")
        return redirect(url_for("index"))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))





if __name__ == '__main__':
    db.create_all()
    app.run()


