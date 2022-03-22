
from extensions import db



class User(db.Model):
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
    num_room = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    features = db.Column(db.String(300), nullable=False)

    def __init__(self, address, district, num_room, price,features):
        self.address = address
        self.district = district
        self.num_room = num_room
        self.price = price
        self.features = features

