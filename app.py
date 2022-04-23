from datetime import timedelta
from os import removedirs
from flask import Flask, jsonify, render_template, request
from flask import send_file
from MySQLdb import Connect, connect
from flask import Flask, config, render_template, request, redirect, url_for, session, flash
from flask.helpers import flash
from flask.typing import ResponseReturnValue
from flask_mysqldb import MySQL
from flask import request
import MySQLdb.cursors
import re
from flask_mail import Mail, Message
import stripe
import os
import datetime
import random
import requests
import string
from time import strftime, localtime
import smtplib
import email.mime.multipart
from email.mime.text import MIMEText
from flask import Flask
from flask_minify import minify
from flask_restful import Resource, Api
import time
import csv
from passlib.hash import sha256_crypt
import pandas as pd
import numpy
from collections import Counter
import gc




stripe_keys = {
    'secret_key': 'sk_test_51JpGWQChgKx4d8ZkeQGxPCSyMNlNUZ3P8PTOKNs7ITsNmdEqlJle6uN4okQaWz1LngjYrj8YXh3Qq8GwQ152sFGW00CTA825OA',
    'publishable_key': 'pk_test_51JpGWQChgKx4d8ZkYMn6qdxfVaPZ3WfVHMhjF3QS5zDgZ214XJea9jPDGFukWXPBjLRxlzsklEheH7vCeYimlljF00zvSYeocw'
}
domain_url = "https://streetviewspectator.com/"
rootPath="/uploads/"
stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)
minify(app=app, html=True, js=True, cssless=True , static=True)
app.secret_key = "Secret Key"
api = Api(app)

# Mysql db config

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fyp'

# Intialize MySQL
mysql = MySQL(app)


# email reset key
key = random.randint(1, 20)
letters = string.ascii_lowercase
final_key = ''.join(random.choice(letters) for i in range(key))




@app.route("/uploads/<path>",methods = ['POST', 'GET'])
def DownloadLogFile (path = None):
        path=os.path.abspath(rootPath+path)
        if path is None:
            return "No File"
        else:
            return send_file(path, as_attachment=True)




@app.route("/", methods=['POST', 'GET'])
def home():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from testimonials")
    data = cursor.fetchall()
    return render_template('index.html', data=data)


@app.route('/pricing')
def price():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT id ,name,description,price,discount, CAST(ROUND((price*12)-(price*12*discount*0.01),2)as SIGNED ) as yearly FROM plans")
    plans = cursor.fetchall()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from testimonials")
    data = cursor.fetchall()
    return render_template('pricing.html', plans=plans, data=data)

@app.route('/upgrade_pricing')
def upgrade_pricing():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select plans.price as current_price from users inner join invoices on users.current_invoice= invoices.id inner join plans on invoices.plan_id = plans.id where users.id=%s",[session['id']])
    data=cursor.fetchone()
    cursor.execute(
        "SELECT id ,name,description,price,discount, CAST(ROUND((price*12)-(price*12*discount*0.01),2)as SIGNED ) as yearly FROM plans where plans.price > %s",[data['current_price']])
    plans = cursor.fetchall()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from testimonials")
    data = cursor.fetchall()
    return render_template('upgrade_pricing.html', plans=plans, data=data)


@app.route('/adminlogin', methods=['POST', 'GET'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        admin = cursor.fetchone()
        # If account exists in accounts table in out database
        if admin:
            session['ad_loggedin'] = True
            session['id'] = admin['id']
            session['username'] = admin['username']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                "select IF(ISNULL(subquery.payment),0,subquery.payment) total from (SELECT sum(IF(invoices.duration>12, plans.discount*0.01*plans.price*invoices.duration, plans.price*invoices.duration)) payment from invoices inner join plans on invoices.plan_id= plans.id where month(invoices.date) = month(CURRENT_TIMESTAMP)) as subquery;")
            plans = cursor.fetchall()
            return redirect(url_for('adminhome'))

        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username/password!", "info")
            return redirect(url_for('login'))

    # Show the login form with message (if any)
    return render_template('adminlogin.html')


# - this will be the home page, only accessible for admin
@app.route('/admin')
def adminhome():
    # Check if user is loggedin
    if 'ad_loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "select IF(ISNULL(subquery.payment),0,subquery.payment) total from (SELECT sum(invoices.total_amount) payment from invoices inner join plans on invoices.plan_id= plans.id where month(invoices.date) = month(CURRENT_TIMESTAMP)) as subquery;")
        t_month = cursor.fetchone()
        cursor.execute(
            "select IF(ISNULL(subquery.payment),0,subquery.payment) total from (SELECT sum(invoices.total_amount) payment from invoices inner join plans on invoices.plan_id= plans.id) as subquery;")
        plans = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) total_active_plans FROM plans where active_status=1;")
        total_active_plans = cursor.fetchone()
        cursor.execute("select count(*) total_users from users")
        total_users = cursor.fetchone()
        cursor.execute("select count(*) active_users from users where  active_status=1")
        active_users = cursor.fetchone()
        cursor.execute(
            "select count(*) new_users from users where month(date_joined) = month(CURRENT_TIMESTAMP) and active_status=1")
        new_users = cursor.fetchone()

        cursor.execute(
            "select count(*) as count, plans.name from users inner join invoices on invoices.id = users.current_invoice INNER JOIN plans on invoices.plan_id= plans.id GROUP BY invoices.plan_id")
        plan = cursor.fetchall()

        return render_template('admindashboard.html', username=session['username'], new_users=new_users,
                               active_users=active_users, t_month=t_month, plans=plans,
                               total_active_plans=total_active_plans, total_users=total_users, plan=plan)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# - this is for view profile for admin
@app.route('/admin/view/admin', methods=['GET', 'POST'])
def adminview():
    if 'ad_loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin')
        Data = cursor.fetchall()
    return render_template('edit_admin.html', data=Data)


# - this is for adit profile for admin just password
@app.route('/admin/edit/admin', methods=['GET', 'POST'])
def adminedit():
    if request.method == 'POST':
        password = request.form['password']
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE admin set  password= %s  WHERE id = %s", (password, id))
        mysql.connection.commit()
        flash("Profile updated Successfully")
        return redirect(url_for('adminview'))


# - this will be the logout page for admin
@app.route('/admin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('ad_loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))


# - this will be the pricing plan page for admin
# - this will be the pricing plan page for admin
@app.route('/admin/plans', methods=["POST", "GET"])
def plans():
    if 'ad_loggedin' in session:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT id ,name,description, num_searches , limits ,price,ROUND(discount) AS discount , ROUND((price*12)-(price*12*discount*0.01)) as yearly FROM plans ORDER BY price ASC;')
        Data = cursor.fetchall()

    else:

        flash("Please Login First")
        return redirect(url_for('login'))

    return render_template('plans.html', plans=Data)


# - this will display users from the database
@app.route('/admin/view/user', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/admin/view/user/page/<int:page>', methods=["POST", "GET"])
def showusers(page):
    if 'ad_loggedin' in session:
        perpage = 4
        startat = (page * perpage) - perpage
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'select users.id, users.username as username , users.email as email , plans.name plan_name, date(invoices.date) start_date,  date(DATE_ADD(invoices.date, INTERVAL invoices.duration DAY)) end_date from users left outer join invoices on users.current_invoice= invoices.id left outer join plans on invoices.plan_id= plans.id order by users.date_joined desc limit %s, %s ',
            (startat, perpage))
        Data = cursor.fetchall()
        cursor.execute('SELECT count(*) as count from users')
        total = cursor.fetchone()
        final = list(range(0, total['count'], perpage))

        if request.method == "POST":
            term = "%" + request.form['search'] + "%"
            perpage = 4
            startat = (page * perpage) - perpage
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'select users.id, users.username as username , users.email as email , plans.name plan_name, date(invoices.date) start_date,  date(DATE_ADD(invoices.date, INTERVAL invoices.duration DAY)) end_date from users left outer join invoices on users.current_invoice= invoices.id left outer join plans on invoices.plan_id= plans.id where users.username LIKE %s order by users.date_joined desc',
                [term])
            Data = cursor.fetchall()
            cursor.execute('SELECT count(*) as count from users')
            total = cursor.fetchone()
            final = list(range(0, total['count'], perpage))
            return render_template('showuser.html', user=Data, total=final, page=page , domain_url=domain_url)
        else:
            return render_template('showuser.html', user=Data, total=final, page=page , domain_url=domain_url)
    else:

        flash("Please Login First")
        return redirect(url_for('login'))


# - Transactions/invoices
@app.route('/admin/view/invoices', defaults={'page': 1})
@app.route('/admin/view/invoices/page/<int:page>', methods=['GET', 'POST'])
def invoices(page):
    if 'ad_loggedin' in session:
        perpage = 4
        startat = (page * perpage) - perpage
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT plans.name as n, date(invoices.date) as d , (CAST(invoices.total_amount as SIGNED)) as t, invoices.payment_status as s,users.username as un  from invoices inner join users on users.id= invoices.user_id inner join plans on invoices.plan_id= plans.id ORDER BY invoices.date DESC limit  %s, %s ',
            (startat, perpage))
        Data = cursor.fetchall()
        cursor.execute('SELECT count(*) as count from invoices')
        total = cursor.fetchone()
        final = list(range(0, total['count'], perpage))

        return render_template('invoices.html',
                               plans=Data,
                               page=page, total=final,
                               domain_url=domain_url
                               )
    else:

        flash("Please Login First")
        return redirect(url_for('login'))


# - this will insert users from the admin panel
@app.route('/admin/add/user', methods=["POST", "GET"])
def addusers():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id , COUNT(*) from users WHERE username=%s AND email=%s", (username, email))
        count = cursor.fetchone()
        total = (str(count['COUNT(*)']))

        if total == "0":

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO users set username=%s, email = %s, password=%s", (username, email, password))
            mysql.connection.commit()
            flash("User Inserted Successfully")
            return redirect(url_for('showusers'))

        else:

            flash("User Already Exists")
            return redirect(url_for('showusers'))

    return redirect(url_for('showusers'))


# edit user
@app.route('/admin/edit/user/', methods=["POST", "GET"])
def editusers():
    if request.method == 'POST':
        email = request.form['email']
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE users set email = %s  WHERE id =%s ", (email, id))
        mysql.connection.commit()

        flash("User Updated")

    return redirect(url_for('showusers'))


# Delete user
@app.route('/admin/delete/user/<id>/', methods=['GET', 'POST'])
def deleteuser(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM users WHERE id = %s', [id])
    mysql.connection.commit()
    flash("User Deleted Successfully")
    # return "Employee Deleted Successfully"

    return redirect(url_for('showusers'))


# this route is for inserting plan from admin dashboard to mysql database via html forms
@app.route('/admin/plans/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        num_searches = request.form['num_searches']
        limits = request.form['limits']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO plans set name=%s, description = %s, num_searches = %s , limits = %s , price=%s",
                       (name, description, num_searches, limits , price))
        mysql.connection.commit()

        flash("Plan Inserted Successfully")

        return redirect(url_for('plans'))


# this route is for editing plan from admin dashboard to mysql database via html forms
@app.route('/admin/plans/edit/', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        discount = request.form['discount']
        num_searches = request.form['num_searches']
        limits = request.form['limits']
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "UPDATE plans set  name= %s, description = %s ,  num_searches = %s ,  limits =%s , price=%s , discount = %s  WHERE id = %s",
            (name, description, num_searches,  limits , price, discount, id))
        mysql.connection.commit()
        flash("Plan updated Successfully")
        return redirect(url_for('plans'))


# - this will be for deleting pricing plan page for admin
@app.route('/admin/plans/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM plans WHERE id = %s', [id])
    mysql.connection.commit()
    flash("Plan Deleted Successfully")
    # return "Employee Deleted Successfully"

    return redirect(url_for('plans'))

@app.route('/user/verify/', methods=['GET', 'POST'])
def user_verify():
    id = request.args.get('id', default=None, type=str)
    if id == None:
        # redirect to get started
        flash("Verification Link is not valid")
        return redirect(url_for('user_login'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select id from users where u_key=%s', [id])
    u_id = cursor.fetchone()

    if u_id == None:
        flash("Verification Link is not valid")
        return redirect(url_for('user_login'))
    else:
        u_id= u_id['id']
        cursor.execute('UPDATE users set is_email_verified=1 where id=%s', [u_id])
        mysql.connection.commit()
        flash("Verification successful")
        return redirect(url_for('user_login'))


    return redirect(url_for('user_login'))
# Admin reset email
@app.route('/adminlogin/reset', methods=['GET', 'POST'])
def sendemail():
    if request.method == 'POST' and 'email' in request.form:
        # Create variables for easy access
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE email = %s ', [email])
        # Fetch one record and return result
        admin = cursor.fetchone()
        # If account exists in accounts table in out database
        if admin:
            email = admin['email']
            msg = Message('Hello from the other side!', sender='flask@codeaza-apps.com', recipients=email)
            url = domain_url + "/adminlogin/password?id="
            final = url + final_key
            with app.app_context():
                msg = Message(
                    subject="Hello",
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=[email],
                    body=final)
            mail.send(msg)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            ts = datetime.datetime.now()
            cursor.execute('SELECT id FROM admin WHERE email = %s', [email])
            id = cursor.fetchone()
            idInt = id['id']
            cursor.execute('INSERT INTO reset VALUES (Null , %s, %s, %s )', (final_key, ts, idInt))
            mysql.connection.commit()
            flash("Email sent Successfully ")
            return redirect(url_for('login'))
        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect email", "info")
            return redirect(url_for('login'))

    return redirect(url_for('login'))


# Admin password email
@app.route('/adminlogin/password', methods=['POST', 'GET'])
def passwordreset():
    id = request.args.get('id')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('select admin_id from reset WHERE secret = %s', [id])
    sk = cursor.fetchone()
    admin_id = (str(sk['admin_id']))

    if request.method == 'POST':
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE admin set password = %s WHERE id = %s ", (password, admin_id))
        mysql.connection.commit()
        flash("Password Updated Successfully ")
        return redirect(url_for('login'))

    return render_template('passwords.html', id=id)


# user routing starts from here onwards

@app.route('/userlogin', methods=['POST', 'GET'])
def user_login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s ', [username])
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in accounts table in out database
        if user:
            print(password, user['password'])
            if not (sha256_crypt.verify(password, user['password'])):
                flash("Incorrect Password", "info")
                return redirect(url_for('user_login'))
            if(user['is_email_verified']==None):
                flash("Please verify your email address before logging in.")
                return redirect(url_for('user_login'))

            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('user_dashboard'))

        else:
            # Account doesnt exist or username/password incorrect
            flash("Incorrect username", "info")
            return redirect(url_for('user_login'))

    # Show the login form with message (if any)
    return render_template('user_login.html')




# user routing -- redirect to register now page.
@app.route('/register', methods=['GET', 'POST'])
def user_register():
    # password = sha256_crypt.encrypt("password")
    # password2 = sha256_crypt.encrypt("password")
    # string= password+", "+ password2+ ", "+ str((sha256_crypt.verify("password", password)))
    # return string

    id = request.args.get('id', default=None, type=str)
    type = request.args.get('type', type=str)
    if id == None:
        # redirect to get started
        return redirect(url_for('price'))
    if type == None:
        # redirect to get started
        return redirect(url_for('price'))
    address2 = None;
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:  # and 'firstname' in request.form and 'lastname' in request.form and 'address1' in request.form:
        # Create variables for easy access
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address1 = request.form['address1']
        address2 = request.form['address2']
        username = request.form['username']
        password = request.form['password']
        password = sha256_crypt.encrypt(password)
        email = request.form['email']
        phone = request.form['phone']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s ', (username, email))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
            return render_template('user_register.html')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table

            invoice_id = None
            if (id is not None):
                cursor.execute('INSERT INTO invoices VALUES (NULL,NULL, "1", "0", current_timestamp(), "1", %s );',
                               [id])
                invoice_id = cursor.lastrowid
            cursor.execute('INSERT INTO users VALUES (NULL, %s,%s,%s,%s,%s, %s, %s, %s , "1" , current_timestamp(), NULL, NULL)',
                           (username, firstname, lastname, address1, address2, email, password, invoice_id))
            userInserted = cursor.lastrowid
            cursor.execute('UPDATE invoices set user_id=%s where id=%s', (userInserted, invoice_id))
            mysql.connection.commit()

            flash('You have successfully registered!', "info")
            return redirect(url_for('user_login'))

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if type == 'monthly':
        cursor.execute('SELECT name , price FROM plans WHERE id = %s', [id])
        data = cursor.fetchone()
        data['plan_id'] = id
        data['subscription_duration'] = 30
    elif type == 'yearly':
        cursor.execute('SELECT name , ROUND((price*12)-(price*12*discount*0.01),0) as price FROM plans WHERE id = %s',
                       [id])
        data = cursor.fetchone()
        data['plan_id'] = id
        data['subscription_duration'] = 30*12
    else:
        return redirect(url_for('price'))

    return render_template('user_register.html', data=data, type=type, key=stripe_keys['publishable_key'])

@app.route('/upgrade_invoice', methods=['GET', 'POST'])
def upgrade_invoice():
    id = request.args.get('id', default=None, type=str)
    type = request.args.get('type', type=str)
    if id == None:
        # redirect to get started
        return redirect(url_for('price'))
    if type == None:
        # redirect to get started
        return redirect(url_for('price'))
    # Show registration form with message (if any)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if type == 'monthly':
        cursor.execute('SELECT name , price FROM plans WHERE id = %s', [id])
        data = cursor.fetchone()
        data['plan_id'] = id
        data['subscription_duration'] = 30
    elif type == 'yearly':
        cursor.execute('SELECT name , ROUND((price*12)-(price*12*discount*0.01),0) as price FROM plans WHERE id = %s',
                       [id])
        data = cursor.fetchone()
        data['plan_id'] = id
        data['subscription_duration'] = 12*30
    else:
        return redirect(url_for('price'))

    return render_template('upgrade_register.html', data=data, type=type, key=stripe_keys['publishable_key'])

# - this will be the logout page for admin
@app.route('/logout')
def user_logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('user_login'))


#model_prediction
def predict(dataset, username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT tweets_prediction.*, tweets.cleaned_content from tweets_prediction inner join tweets on tweets_prediction.tweet_id = tweets.id where tweets.username=%s", [username])
    data= cursor.fetchall()
    df= pd.DataFrame(data)

    #getting top 10 words
    tweets= df['cleaned_content'].values.reshape(-1, 1)
    count_10 = Counter(" ".join(df["cleaned_content"]).split()).most_common(10)

    output1= df
    if(dataset=="humour"):
        output1["tweet"]= tweets
        final=output1['humour'].value_counts()
        return count_10, final, output1
    elif(dataset=="hatespeech_offensive"):
        output1["tweet"]= tweets
        final=output1['hatespeech_offensive'].value_counts()
        return count_10, final, output1
    elif(dataset=="negative_positive_neutral"):
        output1["tweet"]= tweets
        final=output1['negative_positive_neutral'].value_counts()
        return count_10, final, output1




# user routing -- redirect to user dashboard  page.

@app.route("/user_home", methods=['GET', 'POST'])
def user_dashboard():
    if 'loggedin' in session:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        s_id = str(session['id'])


        cursor.execute(
            'SELECT CONCAT(firstname, " ", lastname) AS Name , email ,  active_status  FROM users where id=%s', [s_id])
        user = cursor.fetchone()

        cursor.execute(
            'SELECT date(invoices.date) as date,plans.name as name ,plans.price as price from users inner join invoices on users.current_invoice = invoices.id INNER JOIN plans ON invoices.plan_id=plans.id where users.id= %s',
            [s_id])
        p = cursor.fetchone()
        # //fix amount here

        cursor.execute(
            "SELECT u.current_invoice, i.payment_status,i.plan_id, i.active_status, i.duration as duration from users u left outer join  invoices i on i.id= u.current_invoice where u.id=%s;",
            [s_id])
        Data = cursor.fetchone()
        id=Data['plan_id']
        duration=int(float(Data['duration']))
        amount=0
        if duration == 30:
            cursor.execute('SELECT name , price FROM plans WHERE id = %s',
                           [id])
            data = cursor.fetchone()
        else:
            cursor.execute('SELECT name , ROUND((price*12)-(price*12*discount*0.01),0) as price FROM plans WHERE id = %s',
                           [id])

            data = cursor.fetchone()
        amount=data['price']

        amount = amount * 100
        cursor.execute("SELECT u.current_invoice, i.payment_status, i.active_status, date(DATE_ADD(i.date,interval i.duration DAY))  as date from users u left outer join  invoices i on i.id= u.current_invoice where u.id=%s;",[s_id])
        Data = cursor.fetchone()

        cursor.execute(
            'select p.num_searches as tSearch,p.limits as tLimit from users u inner join invoices i on u.current_invoice=i.id inner join plans p on p.id=i.plan_id  where u.username=%s',
            [session['username']])
        planDetails = cursor.fetchone()

        cursor.execute(
            'select count(*) as count from query where status=1 and user_id=%s',[session['id']]
        )

        queryUsed=cursor.fetchone()


        if request.method == "POST":
            r=requests.get('https://ipinfo.io/'+request.remote_addr+'/json')
            r_data=r.json()
            # country=r_data['region']
            search = request.form['search']
            now = datetime.datetime.now()
            cursor = mysql.connection.cursor()

            if queryUsed['count']<planDetails['tSearch']:
                cursor.execute("select count(*) as count from query where status=0 and user_id=%s;",
                            [session['id']])
                searchLimit=cursor.fetchone()
                if searchLimit[0]>=1:
                    flash("You already have an active search going on, Please wait to finish it first")
                else:
                    cursor.execute("insert into query (id,date,keyword,status,user_id) values (NULL,%s,%s,'1',%s);",
                                (now, search, s_id))
                    mysql.connection.commit()

                    #except:
                    #pass
            else:
                flash("Plan Limit Reached")

        return render_template('user_dashboard.html', user=user, p=p, planDetails=planDetails,queryUsed=queryUsed,Data=Data, key=stripe_keys['publishable_key'], amount=amount)


    else:

        flash("Please Login First")
        return redirect(url_for('user_login'))

    return render_template('user_dashboard.html')


@app.route('/report', methods=['GET', 'POST'])
def showreport():
    username = request.args.get('username', default=None, type=str)
    if username == None:
        return redirect(url_for('search_history'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from users_profile WHERE username=%s", [username])
    user_profile= cursor.fetchone()
    cursor.execute("SELECT count(cleaned_content), MONTH(tweetTS) FROM tweets WHERE UPPER(cleaned_content) LIKE UPPER('%% Spacex %%') GROUP BY MONTH(tweetTS)")
    dates= cursor.fetchall()

    cursor.execute("SELECT tweets_prediction.*, tweets.content, tweets.cleaned_content from tweets_prediction inner join tweets on tweets_prediction.tweet_id = tweets.id where tweets.username=%s", [username])
    tweets_based_prediction = cursor.fetchall()

    df = pd.DataFrame(tweets_based_prediction)
    count = Counter(" ".join(df["cleaned_content"]).split()).most_common(10)
    df['humour'].value_counts()
    a=[df['humour'].value_counts(), df['hatespeech_offensive'].value_counts(), df['negative_positive_neutral'].value_counts()]
    


    data= pd.concat(a)
    data= data.to_dict()
    del a    
    
    return render_template('report.html', humour_data=data, user_profile=user_profile, tweets_based_prediction = tweets_based_prediction, count= count,dates= dates)


# faqs page
@app.route('/faq')
def faq():
    return render_template('faq.html')


# user routing -- redirect to user support page.

@app.route('/user_support', methods=['GET', 'POST'])
def user_support():
    if request.method == "POST":
        name = request.form['name']
        reTo = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        sender = 'support@streetviewspectator.com'
        password1 = 'Codeaza@21'
        body='name: '+name + '<br>' +'email: '+ reTo +'<br>' +reTo+'phone: '+phone+ '<br>'+'message: '+message
        msg = email.mime.multipart.MIMEMultipart()
        msg.add_header('reply-to', reTo)
        msg['subject'] = 'New User Support Ticket | Street View Spectator'
        part1 = MIMEText(body, 'html')
        msg.attach(part1)
        with smtplib.SMTP_SSL('mail.privateemail.com', 465) as smtp:
            smtp.login(sender, password1)
            smtp.sendmail(sender, ['support@streetviewspectator.com'], msg.as_string())
        flash('Message Sent, We will get back to you shortly.!', "info")
        return redirect(url_for('user_support'))

    return render_template('usersupport.html')


# user show search history
@app.route('/search_history', defaults={'page': 1}, methods=['GET', 'POST'])
@app.route('/search_history/<int:page>', methods=['GET', 'POST'])
def search_history(page):
    s_id = str(session['id'])
    perpage = 4
    startat = (page * perpage) - perpage
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'select LTRIM(query.id) as id,CAST(query.Date as DATE) as d, query.keyword, query.status from query where query.user_id= %s order by date desc limit  %s, %s',
            (s_id,startat, perpage))
    Data = cursor.fetchall()
    cursor.execute('SELECT count(*) as count from query where user_id=%s',[session['id']])
    total = cursor.fetchone()
    final = list(range(0, total['count'], perpage))

    if request.method == "POST":

        return render_template('user_history.html', plans=Data , page=page, total=final,
                               domain_url=domain_url)
    return render_template('user_history.html', plans=Data , page=page, total=final,
                               domain_url=domain_url)

# user show transactions
@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    s_id = str(session['id'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        'SELECT invoices.id as invoice, plans.name as n, date(invoices.date) as d ,invoices.total_amount as t, if(invoices.id=users.current_invoice,"Active", "Inactive") as s  from users inner join invoices on users.id= invoices.user_id inner join plans on invoices.plan_id= plans.id where users.id=%s order by date desc',
        [s_id])
    Data = cursor.fetchall()
    cursor
    return render_template('transactions.html', plans=Data, key=stripe_keys['publishable_key'])


def send_email_verification(email, body):
    userInserted = data['id']
    userInserted=int(float(userInserted))
    ran=(random.randint(10000,99999))
    final = str(userInserted)+str(ran)
    hashed_email_verification=(str(hash(final)))
    cur.execute("update users set firstname=%s,lastname=%s,email=%s, is_email_verified=NULL, u_key=%s where id=%s", (fName, lName, email, hashed_email_verification, s_id))
    mysql.connection.commit()


        #send email for verification goes here
    sender = 'support@streetviewspectator.com'
    password1 = 'Codeaza@21'
    subject='New Account Registeration | Street View Spectator'
    body='Hello, Your account information is successfully updated at Street View Spectator.'
    body= body+ 'Your verification link for email is: '+domain_url+'user/verify?id='+hashed_email_verification+' '
    body = body+'Reach out us at support@streetviewspectator.com if you have any queries. Thank You.'
    with smtplib.SMTP_SSL('mail.privateemail.com', 465) as smtp:
        smtp.login(sender, password1)
        msg1 = 'Subject: {}\n\n{}'.format(subject, body)
        smtp.sendmail(sender, [email], msg1)




# user view profile
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    s_id = str(session['id'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from users where id=%s", [s_id])
    data = cursor.fetchone()
    s_id = str(session['id'])
    if request.method == "POST":
        # new_password = request.form['new_password']
        # confirm_password= request.form['confirm_password']
        fName = request.form['fName']
        lName = request.form['lName']
        email = request.form['email']
        cur = mysql.connection.cursor()
        # u_key generation goes here

        if(email!=data['email']):
            cursor.execute('SELECT * FROM users WHERE email = %s', [email])
            # Fetch one record and return result
            user = cursor.fetchone()
            # If account exists in accounts table in out database
            if user:
                flash('Email already exist', "info")
                return redirect(url_for('user_logout'))
            userInserted = data['id']
            ran=(random.randint(10000,99999))
            final = str(userInserted)+str(ran)
            hashed_email_verification=(str(hash(final)))
            u_key="lksjdf"
            cur.execute("update users set firstname=%s,lastname=%s,email=%s, is_email_verified=NULL, u_key=%s where id=%s", (fName, lName, email, hashed_email_verification, s_id))
            mysql.connection.commit()
            sender = 'support@streetviewspectator.com'
            password1 = 'Codeaza@21'
            subject='New Account Registeration | Street View Spectator'
            body='Hello, Your account information is successfully updated at Street View Spectator.'
            body= body+ 'Your verification link for email is: '+domain_url+'user/verify?id='+hashed_email_verification+' '
            body = body+'Reach out us at support@streetviewspectator.com if you have any queries. Thank You.'
            with smtplib.SMTP_SSL('mail.privateemail.com', 465) as smtp:
                smtp.login(sender, password1)
                msg1 = 'Subject: {}\n\n{}'.format(subject, body)
                smtp.sendmail(sender, [email], msg1)


            flash('Profile updated successfully! Email verification link has been sent.', "info")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("select * from users where id=%s", [s_id])
            data = cursor.fetchone()
            return redirect(url_for('user_logout'))
        else:
            cur.execute("update users set firstname=%s,lastname=%s where id=%s", (fName, lName, s_id))

            mysql.connection.commit()
            flash('Profile updated successfully! ', "info")
            return redirect(url_for('profile'))




        #send email for verification goes here

    return render_template('edit_user.html', data=data)




# user view profile
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    s_id = str(session['id'])
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from users where id=%s", [s_id])
    data = cursor.fetchone()
    s_id = str(session['id'])
    if request.method == "POST":
        current_password= request.form['current_password']
        new_password = request.form['new_password']
        confirm_password= request.form['confirm_password']


        cur = mysql.connection.cursor()



        cur.execute("update users set password=%s where id=%s", (new_password, s_id))
        mysql.connection.commit()

        flash('Password updated successfully!', "info")
        return redirect(url_for('user_logout'))
    return render_template('change_password.html', data=data)





# contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        reTo = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        sender = 'support@streetviewspectator.com'
        password1 = 'Codeaza@21'
        body='name: '+name + '<br>' +'email: '+ reTo +'<br>' +'phone: '+phone+ '<br>'+'message: '+message
        msg = email.mime.multipart.MIMEMultipart()
        msg.add_header('reply-to', reTo)
        msg['subject'] = 'New User Support Ticket | Street View Spectator'
        part1 = MIMEText(body, 'html')
        msg.attach(part1)
        with smtplib.SMTP_SSL('mail.privateemail.com', 465) as smtp:
            smtp.login(sender, password1)
            smtp.sendmail(sender, ['support@streetviewspectator.com'], msg.as_string())
        flash('Message Sent, We will get back to you shortly.!', "info")

    return render_template('contact.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from testimonials")
    testi = cursor.fetchall()
    return render_template('about.html', testi=testi)


@app.route('/check_username')
def check_username():
    username = request.args.get('a')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', [username])
    # Fetch one record and return result
    user = cursor.fetchone()
    # If account exists in accounts table in out database
    if user:
        print("Username Already Taken")
        return "0"
    else:
        return "1"


@app.route('/check_email')
def check_email():
    username = request.args.get('a')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', [username])
    # Fetch one record and return result
    user = cursor.fetchone()
    # If account exists in accounts table in out database
    if user:
        print("Username Already Taken")
        return "0"
    else:
        return "1"

@app.route('/check_email_change')
def check_email_change():
    s_id = str(session['id'])
    username = request.args.get('a')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * from users WHERE id=%s',[s_id])
    data=cursor.fetchone()
    previous_email=data['email']
    cursor.execute('SELECT * FROM users WHERE email = %s', [username])
    # Fetch one record and return result
    user = cursor.fetchone()
    # If account exists in accounts table in out database
    if user:
        if(username==previous_email):
            return "1"
        print("Username Already Taken")
        return "0"
    else:
        return "1"



@app.route("/admin/testimonial", methods=['POST', 'GET'])
def testimonial_view():
    if 'ad_loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * from testimonials")
        data = cursor.fetchall()
        return render_template("testimonial_admin.html", data=data)

    return render_template("testimonial_admin.html")


@app.route('/admin/testimonial/add', methods=['POST', 'GET'])
def testimonial_admin_add():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        designation = request.form['designation']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO testimonials set name=%s, description = %s, designation = %s",
                       (name, description, designation))
        mysql.connection.commit()
        flash("Testimonial Added Successfully")

        return redirect(url_for('testimonial_view'))


@app.route("/admin/testimonial/delete/<id>", methods=['POST', 'GET'])
def testimonial_delete(id):
    if 'ad_loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM testimonials WHERE id = %s", [id])
        data = cursor.fetchone()
        mysql.connection.commit()
        flash("Testimonial Deleted Successfully")

        return redirect(url_for('testimonial_view'))


@app.route('/admin/testimonial/edit/', methods=['GET', 'POST'])
def testimonial_edit():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        designation = request.form['designation']
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE testimonials set  name=%s, description=%s , designation=%s WHERE id =%s",
                       (name, description, designation, id))
        mysql.connection.commit()
        flash("Testimonial Updated Successfully")
        return redirect(url_for('testimonial_view'))


# search query pass


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = request.form['amount']

    hogaya = False
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:  # and 'firstname' in request.form and 'lastname' in request.form and 'address1' in request.form:
        # Create variables for easy access
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        password = request.form['password']
        password = sha256_crypt.encrypt(password)
        email = request.form['email']
        id = request.form['plan_id']
        plan_duration = request.form['plan_duration']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s ', (username, email))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
            return redirect(url_for('user_login'))
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            hogaya = True
            # Account doesnt exists and the form data is valid, now insert new account into accounts table


    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)

    data = {}
    data['amount'] = amount

    amount = int(float(amount))
    amount = amount * 100
    try:
        if(amount>0):
            customer = stripe.Customer.create(
                email='customer@example.com',
                source=request.form['stripeToken']
            )
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=amount,
                currency='usd',
                description='Flask Charge'
            )
        if hogaya:
            invoice_id = None
            if (id is not None):
                cursor.execute('INSERT INTO invoices VALUES (NULL,NULL, "1", "0", current_timestamp(), %s, %s, %s );',
                               (plan_duration, id, data['amount']))
                invoice_id = cursor.lastrowid
            cursor.execute('INSERT INTO users VALUES (NULL, %s,%s,%s, %s, %s, %s , "1" , current_timestamp(), NULL, NULL)',
                           (username, firstname, lastname,email, password, invoice_id))
            userInserted = cursor.lastrowid
            ran=(random.randint(10000,99999))
            final = str(userInserted)+str(ran)
            hashed_email_verification=(str(hash(final)))
            cursor.execute('UPDATE users set u_key=%s where id=%s',(hashed_email_verification, userInserted))
            cursor.execute('UPDATE invoices set user_id=%s where id=%s', (userInserted, invoice_id))
            mysql.connection.commit()
            sender = 'support@streetviewspectator.com'
            password1 = 'Codeaza@21'
            subject='New Account Registeration | Street View Spectator'
            body='Hello We are happy to have you, Your account is successfully registered at Street View Spectator.'
            body= body+ 'Your verification link for email is: '+domain_url+'user/verify?id='+hashed_email_verification+' '
            body = body+'Reach out us at support@streetviewspectator.com if you have any queries. Thank You.'
            with smtplib.SMTP_SSL('mail.privateemail.com', 465) as smtp:
                smtp.login(sender, password1)
                msg1 = 'Subject: {}\n\n{}'.format(subject, body)
                smtp.sendmail(sender, [email], msg1)

            flash('You have successfully registered!', "info")
            return redirect(url_for('user_login'))
            pass
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

        print("Card Declined")
        flash('Card Declined:  %s' % e.user_message)
        return redirect(url_for('price'))
    # Use Stripe's library to make requests...
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        flash('Payment Failed due to too many requests. Please try again later')
        return redirect(url_for('price'))
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        print(e)
        return redirect(url_for('price'))
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        flash('Payment Failed due to an Invalid Authentication. Please contact support.')
        return redirect(url_for('price'))
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('price'))
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('price'))
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print("Card Declined %s", e)
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('price'))

    return render_template('charge.html', data=data)

#charge to upgrade


@app.route('/upgrade_charge', methods=['POST'])
def upgrade_charge():

    s_id = str(session['id'])
    # Amount in cents
    amount = request.form['amount']
    hogaya = False
        # Create variables for easy access
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    id = request.form['plan_id']
    plan_duration = request.form['plan_duration']
    hogaya = True
    # Account doesnt exists and the form data is valid, now insert new account into accounts table
    data = {}
    data['amount'] = amount

    amount = int(float(amount))
    amount = amount * 100
    try:
        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )
        if hogaya:
            invoice_id = None
            if (id is not None):
                cursor.execute('INSERT INTO invoices VALUES (NULL,%s, "1", "1", current_timestamp(), %s, %s, %s );', (s_id, plan_duration, id, data['amount']))
                invoice_id = cursor.lastrowid
                cursor.execute("UPDATE users set current_invoice= %s where id=%s",(invoice_id, s_id))
                mysql.connection.commit()
                flash('You have successfully renewed')
                return redirect(url_for('user_dashboard'))
                pass
            else :
                flash('Error Upgrading your plan')
                return redirect(url_for('user_dashboard'))
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

        print("Card Declined")
        flash('Card Declined:  %s' % e.user_message)
        return redirect(url_for('user_dashboard'))
    # Use Stripe's library to make requests...
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        flash('Payment Failed due to too many requests. Please try again later')
        return redirect(url_for('user_dashboard'))
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        flash('Payment Failed due to an Invalid Authentication. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print("Card Declined %s", e)
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))

    return render_template('charge.html', data=data)
@app.route('/renew', methods=['POST'])
def renew():
    data = {}

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    s_id = str(session['id'])

    cursor.execute(
        "SELECT u.current_invoice, i.payment_status,i.plan_id, i.active_status, i.duration as duration from users u left outer join  invoices i on i.id= u.current_invoice where u.id=%s;",
        [s_id])
    Data = cursor.fetchone()
    id=Data['plan_id']
    duration = int(float(Data['duration']))
    if duration==30:
        cursor.execute('SELECT name , price FROM plans WHERE id = %s',
                       [id])
        data = cursor.fetchone()
    else:

        cursor.execute('SELECT name , ROUND((price*12)-(price*12*discount*0.01),0) as price FROM plans WHERE id = %s',
                       [id])
        data = cursor.fetchone()
    amount=data['price']
    cursor.execute(
        'SELECT CONCAT(firstname, " ", lastname) AS Name , email ,  active_status  FROM users where id=%s', [s_id])
    user = cursor.fetchone()

    cursor.execute(
        'SELECT plans.id as plan_id, date(invoices.date) as date,plans.name as name ,plans.price as price from invoices INNER JOIN plans ON invoices.plan_id=plans.id where invoices.user_id= %s',
        [s_id])
    p = cursor.fetchone()

    cursor.execute(
        'select p.num_searches as tSearch,p.limits as tLimit from invoices i inner join users u on u.id=i.user_id inner join plans p on p.id=i.plan_id  where u.username=%s',
        [session['username']])
    planDetails = cursor.fetchone()

    cursor.execute(
        'select count(*) as count from query where status=1 and user_id=%s',[session['id']]
    )

    queryUsed=cursor.fetchone()

    amount = int(float(amount))
    amount = amount * 100
    hogaya=1;
    try:
        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )
        if hogaya:
            invoice_id = None
            if (id is not None):
                cursor.execute('INSERT INTO invoices VALUES (NULL,%s, "1", "1", current_timestamp(), %s, %s, %s );',
                               (s_id, Data['duration'], p['plan_id'], (amount/100)))
                invoice_id = cursor.lastrowid
            cursor.execute("UPDATE users set current_invoice= %s where id=%s",(invoice_id, s_id))
            mysql.connection.commit()
            flash('You have successfully renewed')
            return redirect(url_for('user_dashboard'))
            pass
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

        print("Card Declined")
        flash('Card Declined:  %s' % e.user_message)
        return redirect(url_for('user_dashboard'))
    # Use Stripe's library to make requests...
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        flash('Payment Failed due to too many requests. Please try again later')
        return redirect(url_for('user_dashboard'))
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        flash('Payment Failed due to an Invalid Authentication. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print("Card Declined %s", e)
        print("Amount: %s",amount )
        flash('Payment Failed due to an Invalid Request. Please contact support.')
        return redirect(url_for('user_dashboard'))

    return render_template('charge.html', data=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
    app.debug = True
