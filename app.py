from flask import Flask, request, render_template, url_for, redirect, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib

app = Flask(__name__)
app.secret_key = '12345'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pythonlogin'
mysql = MySQL(app)


@app.route('/')
def hello_world():
    app.logger.info("Rendering home page")
    print('Hello')
    return render_template("index.html")


@app.route('/about')
def about():
    app.logger.info("Displaying about us page")
    return render_template("about.html")


@app.route('/shop')
def shop():
    app.logger.info("Displaying shop page")
    return render_template("shop.html")


@app.route('/story')
def story():
    app.logger.info("Rendering story page")
    return render_template("story.html")


@app.route('/login')
def login_home():
    app.logger.info("Rendering login form")
    return render_template("profile/index.html")


@app.route('/login_submit', methods=['POST'])
def login_submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        street = request.form['street']
        city = request.form['city']
        postal_code = request.form['postal_code']
        password = request.form['password']
        birth_date = request.form['birth_date']

        # Add your logic to insert the user into the database or perform login verification
        # For simplicity, I'll just print the values for now
        print(f'First Name: {first_name}')
        print(f'Last Name: {last_name}')
        print(f'Email: {email}')
        print(f'Phone: {phone}')
        print(f'Street: {street}')
        print(f'City: {city}')
        print(f'Postal Code: {postal_code}')
        print(f'Password: {password}')
        print(f'Birth Date: {birth_date}')

        return 'Data received!'
    else:
        return redirect(url_for('login_home'))


if __name__ == '__main__':
    app.run()
