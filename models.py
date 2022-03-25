from flask_login import UserMixin

from extensions import db



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username




class Listing(db.Model):
    __tablename__ = 'listings'

    house_ID = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=False)
    district = db.Column(db.String(120), nullable=False)
    type_room = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    features = db.Column(db.String(300), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)

    def __init__(self, address, district, type_room, price, features, owner_id):
        self.address = address
        self.district = district
        self.type_room = type_room
        self.price = price
        self.features = features
        self.owner_id = owner_id

