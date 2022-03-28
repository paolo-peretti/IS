from flask_login import UserMixin

from extensions import db



class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type_user = db.Column(db.String(80), nullable=False)

    def __init__(self, username, email, password, name, type_user):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.type_user = type_user

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



class Message(db.Model):
    __tablename__ = 'messages'

    message_ID = db.Column(db.Integer, primary_key=True)
    user1_ID = db.Column(db.String(120), nullable=False) # who sent the message
    user2_ID = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(600), nullable=False)


    def __init__(self, user1_ID, user2_ID, message):
        self.user1_ID = user1_ID
        self.user2_ID = user2_ID
        self.message = message
