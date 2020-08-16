import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from alpha_vantage.timeseries import TimeSeries
from configparser import ConfigParser

config = ConfigParser()

config.read(os.getcwd() + os.path.sep + "config.ini")
alpha_key = config.get('config', 'key')


timeseries = TimeSeries(key=alpha_key)

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    # Points where to look for the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # Tells the app to not track all the modifications to the database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(32)

    db.init_app(app)

    # Initialize the login for the users
    from flaskr.models import load_user
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    # Initialize the routes for the website
    from flaskr.endpoints import routes
    app.register_blueprint(routes)

    return app
