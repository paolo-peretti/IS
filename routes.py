from flask import render_template, request, session, flash, url_for
from extensions import app




@app.route('/')
def index():
    return render_template('./templates/index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/user', methods=['GET', 'POST'])
def user():

    email = None
    if "user" in session:
        user = session["user"]

        if request.method == 'POST':

            email = request.form['email']
            session['email'] = email

            flash('Email was saved!')

        else:
            if "email" in session:
                email = session['email']


        return render_template('index.html', email=email)

    else:

        flash('You are not logged in!')
        return render_template(url_for('login'))