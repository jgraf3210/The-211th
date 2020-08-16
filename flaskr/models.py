from flask import Flask
from flaskr import db, login_manager
from flask_login import UserMixin
from random import randint
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


# Database model for the User entries
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(20), nullable=False)
    last_name = db.Column(db.VARCHAR(30), nullable=False)
    email = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    pass_hash = db.Column(db.VARCHAR(100), nullable=False)
    username = db.Column(db.VARCHAR(25), unique=True, nullable=False)

    # Functions to return values
    def get_id(self):
        return self.id

    def get_email(self):
        return self.email

    def get_pass_hash(self):
        return self.pass_hash

    def get_username(self):
        return self.username

    # In-case the user has to change their password
    def set_password(self, password):
        self.pass_hash = generate_password_hash(password,
                                                method='sha256')

    # Check if the input password matches the stored password hash
    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __init__(self, first_name, last_name, email, pass_hash, username):
        used = True
        # Generate a random id for the new user
        while(used):
            rand = randint(1, 4294967295)
            # If the number is not in use then the id id valid
            # Else run the random number again
            if (db.session.query(User).filter_by(id=rand).first() == None):
                used = False
        self.id = rand
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.pass_hash = pass_hash
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Stock(db.Model):
    stock_id = db.Column(db.Integer, primary_key=True, nullable=False)
    stock_name = db.Column(db.VARCHAR(30), unique=True, nullable=False)
    ticker = db.Column(db.VARCHAR(10), unique=True, nullable=False)

    def __init__(self, stock_id, stock_name, ticker):
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.ticker = ticker


class StockDaily(db.Model):
    stock_id = db.Column(db.Integer, primary_key=True, nullable=False)
    stock_symbol = db.Column(db.VARCHAR(10), nullable=False)
    open_price = db.Column(db.REAL, nullable=False)
    high_price = db.Column(db.REAL, nullable=False)
    low_price = db.Column(db.REAL, nullable=False)
    close_price = db.Column(db.REAL, nullable=False)
    date = db.Column(db.Date, nullable=False)
    volume = db.Column(db.Integer, nullable=False)

    def __init__(self, stock_id, stock_symbol, open_price, high_price, low_price, close_price, date, volume ):
        self.stock_id = stock_id
        self.stock_symbol = stock_symbol
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.date = date
        self.volume = volume


class Prediction(db.Model):
    stock_id = db.Column(db.Integer, primary_key=True, nullable=False)
    predicted_value = db.Column(db.REAL, nullable=False)
    confidence_value = db.Column(db.REAL, nullable=False)
