from flask import Flask, flash, request, render_template, jsonify
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import re

app =Flask(__name__)

@app.route('/')
def index():
    if request.method == 'GET':
        msg = "Hello World"
        return jsonify({'Message':msg})

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'GET':
        msg = 'Please fill out the form !'
        return jsonify([{'errorMessage':msg}])
    if request.method == 'POST' and 'username' in request.get_json() and 'password' in request.get_json() and 'email' in request.get_json():
        content = request.get_json()
        company_legal_name = content['companyLegalName']
        company_name = content['companyName']
        username = content['username']
        email = content['email']
        phone_number = content['phoneNumber']
        password = content['password']
        confrim_password = content['confrimPassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE (username = % s OR email = % s OR phone_number = % s OR company_legal_name = % s', (username, email, phone_number, company_legal_name, ))
        account = cursor.fetchone()

        # initialize regex to the regex expression.
        # this regex is more roburst for email validation than [^@]+@[^@]+\.[^@]+
        regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

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
        elif password != confrim_password:
            msg = 'Password does not match confirmation'
            return jsonify({'errorMessage':msg})
        else:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s)', (company_legal_name, company_name, username, email, phone_number, password_hash, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return jsonify({'Message':msg,'status': 200})
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return jsonify({'errorMessage':msg})

if __name__ == "__main__":
    app.run(debug=True