
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

# __name__ represents the name of the application package and it's used by Flask to identify resources like templates, static assets and the instance folder.
app = Flask(__name__)

app.secret_key = 'hello'

# we are setting the database in which we are working
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/IS"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# we need to pass the Flask app to this method to interact with the database.
db = SQLAlchemy(app)
