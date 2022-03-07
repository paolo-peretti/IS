from flask import render_template, request, session, flash, url_for, redirect
from extensions import app



@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/<usr>')
# def user(usr):
#     return 'hello '+usr


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]

        session["user"] = username

        return redirect(url_for("user"))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route('/user')
def user():

    email = None

    # session["user"] = username
    if "user" in session:

        user = session["user"]

        return 'hello '+user


        return render_template('index.html', email=user)

    else:

        flash('You are not logged in!')
        return redirect(url_for("login"))



if __name__ == '__main__':
    app.run()


