from flask import render_template, redirect, flash, request, url_for, Blueprint
from flaskr.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_required, login_user, logout_user
from flaskr.models import User
from werkzeug.security import generate_password_hash
from flaskr import db, cnxn
import os
import json

sep = os.path.sep

# Defines all the routes for the website
routes = Blueprint('routes', __name__)

######################################################################################################
### CODE FOR CALLING DB AND PARSING INTO JSON OBJECT TO BE PASSED INTO JAVASCRIPT ###

#****************GET DATA FOR A SINGLE STOCK**********************
msft_data = []
aapl_data = []
googl_data = []

#Type in the symbol for what data you want
symbols = ['MSFT', 'AAPL', 'GOOGL']

def create_objects(symbol):
    data = []
    cursor = cnxn.cursor()
    query = "SELECT * FROM StockAdviseDB.dbo.MAIN WHERE SYMBOL = '%s';" % symbol
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.commit()

    for row in rows:
        data.append([x for x in row])
    jdata = json.dumps(data, indent=4)
    ndata = json.loads(jdata)

    data_obj = []
    for row in ndata:
        dict_row = {
            "symbol": '"' + row[1] + '"',
            "date": '"' + row[2] + '"',
            "close": row[6],
        }
        data_obj.append(dict_row)

    stock_data = str(data_obj)
    return stock_data

def get_prediction(symbol):
    cursor = cnxn.cursor()
    query = "SELECT PREDICTED_CLOSE, CONFIDENCE_VAL FROM StockAdviseDB.dbo.Predictions WHERE SYMBOL = '%s';" % symbol
    cursor.execute(query)
    prediction = cursor.fetchall()
    cursor.commit()
    return prediction[0]

#Confidence Value For Stocks
msft_con = round(get_prediction('MSFT')[1], 2)
aapl_con = round(get_prediction('AAPL')[1], 2)
googl_con = round(get_prediction('GOOGL')[1], 2)

#Predictions For Stocks
msft_pred = round(get_prediction('MSFT')[0], 2)
aapl_pred = round(get_prediction('AAPL')[0], 2)
googl_pred = round(get_prediction('GOOGL')[0], 2)

#Data For Stocks
msft_data = create_objects('MSFT')
aapl_data = create_objects('AAPL')
googl_data = create_objects('GOOGL')


######################################################################################################
# Home page endpoint
@routes.route("/")
def home():
    return render_template("home.html")


@routes.route("/about")
def about():
    return render_template("about.html")


@routes.route("/contact")
def contact():
    return render_template("contact.html")

#Routes to page with D3 Graphs, currently displays data as a variable
@routes.route("/services")
def services():
    # microsoft_data = msft_data
    return render_template("services.html",
                           microsoft_data=msft_data,
                           google_data=googl_data,
                           apple_data=aapl_data,
                           msft_pred=msft_pred,
                           aapl_pred=aapl_pred,
                           googl_pred=googl_pred,
                           msft_con=msft_con,
                           aapl_con=aapl_con,
                           googl_con=googl_con)


# Route for the products page
@routes.route("/products")
def products():
    return render_template("products.html")


# Endpoint for the login page and user login
@routes.route("/login", methods=['GET', 'POST'])
def login():
    # redirect to the home page if the user is already logged in
    if( current_user.is_authenticated ):
        return redirect(url_for('routes.home'))
    form = LoginForm(request.form)
    # If the user is trying to log in
    if( form.validate_on_submit() ):
        print('Login request')
        # Search for the username in the database
        user = User.query.filter_by(username=form.username.data).first()
        # If the user is not found or the password is incorrect
        if( user is None or not user.check_password(form.password.data) ):
            flash('Invalid user information')
            return redirect(url_for('routes.login'))
        # Log in the user (Only reaches here if the information is valid)
        login_user(user)
        return redirect(url_for('routes.home'))
    # If the user is opening the webpage
    else:
        return render_template("login.html", form=form)


# Endpoint for user logout
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))


# Route for the register page
@routes.route("/register", methods=['GET', 'POST'])
def register():
    if( current_user.is_authenticated ):
        return redirect(url_for('routes.home'))
    form = RegistrationForm(request.form)
    # If the user is trying to register
    if( form.validate_on_submit() ):
        print('Register request')
        # Checks that the information in the form is valid
        valid = True
        if (check_for_dup_email(form.email.data)):
            valid = False
            flash('That email is already taken', 'email')
        if (check_for_dup_username(form.username.data)):
            valid = False
            flash('That username is already taken', 'username')
        print(valid)
        if(valid):
            try:
                user = User(first_name=form.firstname.data,
                            last_name=form.lastname.data,
                            email=form.email.data,
                            username=form.username.data,
                            pass_hash=generate_password_hash(form.password.data))
                # Add the user account into the database
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('routes.login'))
            except:
                return "There was an issue getting you registered"
        else:
            return render_template("register.html", form=form)
    # If the user is visiting the webpage
    else:
        return render_template("register.html", form=form)


# Route for 500 errors
@routes.errorhandler(500)
def database_error(e):
    return "500 Error page"


# Route for 404 errors
@routes.errorhandler(404)
def page_not_found(e):
    return "404 Error page"


# Endpoint for user profiles
@routes.route('/profile')
@login_required
def profile():
    if(current_user.is_authenticated):
        return render_template('userPage.html')
    return redirect(url_for('routes.home'))

# Route for deleting a user
@routes.route('/delete')
@login_required
def delete_user():
    print('Delete user endpoint in development')
    return'Delete user endpoint in development'


@routes.route('/forgot')
def forgot_password():
    return 'Forgotten password service in development'


# Checks to see if there are duplicate emails
def check_for_dup_email(email):
    if (db.session.query(User).filter_by(email=email).first() == None):
        # Valid information
        return False
    # Invalid information
    return True


# Checks to see if there are duplicate emails
def check_for_dup_username(username):
    if (db.session.query(User).filter_by(username=username).first() == None):
        # Valid information
        return False
    # Invalid information
    return True
