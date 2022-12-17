from flask import Flask, flash, request, render_template, jsonify, session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import re
import pymysql
import secrets_1
# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
# from sqlalchemy import create_engine

# conn = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(secrets_1.user, secrets_1.password, secrets_1.host, secrets_1.port, secrets_1.database)
# app =Flask(__name__)
# app.config['SECRET_KEY']='73f0bb82bf00b8420f2b54077e68ad5f266dd1911b6b3a83'
# app.config["SQLALCHEMY_DATABASE_URI"] = conn
# db = SQLAlchemy(app)
  
# connect the database
# engine = create_engine(url=f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
# conn = engine.connect()

# create flask app, set secret key and configure database
app = Flask(__name__)
app.config['SECRET_KEY'] = '29c60916714c8b899ca90061bbcffa200e6ce2d567788a9c'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///user.db'
db = SQLAlchemy(app)
# instantiate the marshmallow
ma = Marshmallow(app)

# create a class that has the same name as the mysql server already created
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyLegalName = db.Column(db.String(100))
    companyName = db.Column(db.String(100))
    username = db.Column(db.String(42))
    email = db.Column(db.String(60))
    phoneNumber = db.Column(db.String(20))
    password = db.Column(db.String(100))

    def __repr__(self):
        return self.name

with app.app_context():
    db.create_all()


class AccountSchema(ma.Schema):
    class Meta:
        fields = ('id', 'companyLegalName', 'companyName', 'username', 'email', 'pnoneNumber', 'password')

@app.route('/')
def index():
    if request.method == 'GET':
        msg = "Hello World"
        account = Accounts.query.all()
        account_schema = AccountSchema(many=True)
        output = account_schema.dump(account)
        return jsonify({'Product': output})

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'GET':
        msg = 'Please fill out the form !'
        return jsonify([{'errorMessage':msg}])
    if request.method == 'POST':
        if 'username' in request.get_json() and 'password' in request.get_json() and 'email' in request.get_json():
            content = request.get_json()
            company_legal_name = content['companyLegalName']
            company_name = content['companyName']
            username = content['username']
            email = content['email']
            phone_number = content['phoneNumber']
            password = content['password']
            confirm_password = content['confirmPassword']

            # initialize regex to the regex expression.
            # this regex is more roburst for email validation than [^@]+@[^@]+\.[^@]+
            regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
            account = Accounts.query.filter_by(email=email, username=username, companyName=company_name).first()
            # checks if user email, username phone number or company name already exists
            if account:
                msg = 'Account already exists !'
            elif not re.fullmatch(regex, email):
                msg = 'Invalid email address !'
                return jsonify({'errorMessage':msg})
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
                return jsonify({'errorMessage':msg})
            elif not re.match(r'[A-Za-z0-9]+', password) and len(password) < 6:
                msg = 'Pasword must at least 6, at least 1 character(s) and number(s)!'
                return jsonify({'errorMessage':msg})
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
                return jsonify({'errorMessage':msg})
            elif password != confirm_password:
                msg = 'Password does not match confirmation'
                return jsonify({'errorMessage':msg})
            else:
                password_hash = generate_password_hash(password)
                form = Accounts(companyLegalName=company_legal_name, companyName=company_name, username=username, email=email, phoneNumber=phone_number, password=password_hash)
                db.session.add(form)
                db.session.commit()
                print(form)
                msg = 'You have successfully registered !'
                return jsonify({'Message':msg,'status': 200})
        else:
            msg = 'Please fill out the form !'
            return jsonify([{'errorMessage':msg}])

if __name__ == "__main__":
    app.run(debug=True)