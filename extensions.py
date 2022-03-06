
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = 'hello'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/IS"

db = SQLAlchemy(app)
