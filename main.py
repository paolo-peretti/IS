from flask import render_template, request, session, flash, url_for, redirect
from extensions import app



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

        return redirect(url_for("index"))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))






if __name__ == '__main__':
    app.run()


