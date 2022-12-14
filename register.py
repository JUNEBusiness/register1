from flask import Flask, flash, request, render_template, redirect
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
import re


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        company_legal_name = request.form['companyLegalName']
        company_name = request.form['companyName']
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phoneNumber']
        password = request.form['password']
        confrim_password = request.form['confrimPassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE (username = % s OR email = % s OR phone_number = % s OR company_legal_name = % s', (username, email, phone_number, company_legal_name, ))
        account = cursor.fetchone()

        # initialize regex to the regex expression.
        # this regex is more robust for email validation than [^@]+@[^@]+\.[^@]+
        regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

        # checks if user email, username phone number or company name already exists
        if account:
            msg = 'Account already exists !'
        elif not re.fullmatch(regex, email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', password) and len(password) < 6:
            msg = 'Pasword must at least 6, at least 1 character(s) and number(s)!'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        elif password != confrim_password:
            msg = 'Password does not match confirmation'
        else:
            password_hash = generate_password_hash(password)
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s)', (company_legal_name, company_name, username, email, phone_number, password_hash, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)