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
    description = db.Column(db.String(1200))

    def __init__(self, username, email, password, name, type_user, description):
        self.username = username
        self.email = email
        self.password = password
        self.name = name
        self.type_user = type_user
        self.description = description

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
    user1_ID = db.Column(db.Integer, nullable=False) # who sent the message
    user2_ID = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(1200), nullable=False)


    def __init__(self, user1_ID, user2_ID, message):
        self.user1_ID = user1_ID
        self.user2_ID = user2_ID
        self.message = message



class Review(db.Model):
    __tablename__ = 'reviews'

    review_ID = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer, nullable=False) # user
    listing_ID = db.Column(db.Integer, nullable=False) # could be the listing
    text = db.Column(db.String(1200), nullable=False)
    num_flag = db.Column(db.Integer, nullable=False)


    def __init__(self, user_ID, listing_ID, text, num_flag):
        self.user_ID = user_ID
        self.listing_ID = listing_ID
        # self.type_receiver = type_receiver
        self.text = text
        self.num_flag = num_flag



class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.Integer, nullable=False) # user
    listing_ID = db.Column(db.Integer, nullable=False) # could be the listing


    def __init__(self, user_ID, listing_ID):
        self.user_ID = user_ID
        self.listing_ID = listing_ID
