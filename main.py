from flask import render_template, request, session, flash, url_for, redirect
from extensions import app



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<usr>')
def user(usr):
    return 'hello '+usr


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("user", usr=username))
    else:
        return render_template('login.html')


# @app.route('/user')
# def user():
#
#     email = None
#     if "user" in session:
#         user = session["user"]
#
#         if request.method == 'POST':
#
#             email = request.form['email']
#             session['email'] = email
#
#             flash('Email was saved!')
#
#         else:
#             if "email" in session:
#                 email = session['email']
#
#
#         return render_template('index.html', email=email)
#
#     else:
#
#         flash('You are not logged in!')
#         # return render_template('index.html', email=email)
#         return redirect(url_for("index"))



if __name__ == '__main__':
    app.run()


