import time

import psycopg2
import socket
from flask import Flask, request, render_template, redirect, session, jsonify, url_for
from flask_session import Session
from datetime import datetime
import requests

server_hostname = "srv-cn5lbkgl5elc73e7hus0-hibernate-689d6995f9-v54tm"

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def connect_to_database():
    # Connection string for PostgreSQL

    if socket.gethostname() == server_hostname:
        connection_string = "postgres://postgresql:Mre24ol0TQsfbyMY7AmiHxFaiMW5qTZ2@dpg-cn52h90l6cac73a8vvu0-a/doodlewear"
    else:
        connection_string = "dbname=doodlewear user=postgresql password=Mre24ol0TQsfbyMY7AmiHxFaiMW5qTZ2 host=dpg-cn52h90l6cac73a8vvu0-a.frankfurt-postgres.render.com port=5432"

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(connection_string)
    return conn

def create_cursor(conn):
    return conn.cursor()

def get_user_info(cursor, username):
    query = "SELECT * FROM users WHERE username ILIKE %s"
    cursor.execute(query, (username,))

    results = cursor.fetchall()

    if results:
        columns = ['id', 'username', 'password', 'birth_date', 'email', 'phone_number', 'street', 'house_number', 'city', 'postal_code', 'country', 'role']
        return [dict(zip(columns, row)) for row in results]
    else:
        return None


def register_user(cursor, username, first_name, last_name, email, phone, street, house_number, city, postal_code, country, password, birth_date):
    # Check if the username already exists (case-insensitive)
    check_query = "SELECT * FROM users WHERE LOWER(username) = LOWER(%s)"
    cursor.execute(check_query, (username.lower(),))
    existing_user = cursor.fetchone()

    if existing_user:
        # Username already exists, handle accordingly (e.g., raise an exception or return an error)
        raise ValueError("Username already exists")

    # Convert birth_date to a date object
    birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()

    # Insert the new user
    insert_query = """
        INSERT INTO users (
            username, first_name, last_name, email, phone_number, street, house_number, city, postal_code, country, password, birth_date, role
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'user'
        )
    """
    cursor.execute(insert_query, (
        username.lower(), first_name, last_name, email, phone, street, house_number, city, postal_code, country, password, birth_date_obj
    ))

def change_username(cursor, old_username, new_username):
    # Check if the new username already exists (case-insensitive)
    check_query = "SELECT * FROM users WHERE LOWER(username) = LOWER(%s)"
    cursor.execute(check_query, (new_username.lower(),))
    existing_user = cursor.fetchone()

    if existing_user:
        # New username already exists, handle accordingly (e.g., raise an exception or return an error)
        raise ValueError("New username already exists")

    # Update the username
    update_query = """
        UPDATE users SET username = LOWER(%s) WHERE LOWER(username) = LOWER(%s)
    """
    cursor.execute(update_query, (new_username.lower(), old_username.lower()))

def change_password(cursor, username, old_password, new_password):
    # Check if the old password matches the password in the database
    check_query = "SELECT * FROM users WHERE LOWER(username) = LOWER(%s)"
    cursor.execute(check_query, (username,))
    user = cursor.fetchone()

    if user and user[2].strip() == old_password.strip():  # Assuming password is at index 2
        # Update the password
        update_query = """
            UPDATE users SET password = %s WHERE LOWER(username) = LOWER(%s)
        """
        cursor.execute(update_query, (new_password, username))
    else:
        raise ValueError("Invalid old password")

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/shop')
def shop():
    return render_template("shop.html")

@app.route('/story')
def story():
    return render_template("story.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = connect_to_database()
        cursor = create_cursor(connection)
        user_info_list = get_user_info(cursor, username)
        cursor.close()
        connection.close()
        if user_info_list:
            for user_info in user_info_list:
                print("User Info:", user_info)  # Print user information for debugging
                if password == user_info['password']:
                    session["name"] = username
                    return redirect("/profile")
            response_data = {}
            return render_template("profile/index.html", response_data=response_data)
        response_data = {}
        return render_template("profile/index.html", response_data=response_data)
    response_data = {}
    return render_template("profile/index.html", response_data=response_data)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        street_house_number = request.form.get("street")
        city = request.form.get("city")
        postal_code = request.form.get("postal_code")
        password = request.form.get("password")
        birth_date = request.form.get("birth_date")

        address = street_house_number.split(" ")
        street = address[0]
        house_number = address[1]

        try:
            connection = connect_to_database()
            cursor = create_cursor(connection)

            # Call the register_user function with case-insensitive username
            register_user(cursor, username, first_name, last_name, email, phone, street, house_number, city,
                          postal_code, 'switzerland', password, birth_date)
            connection.commit()
            cursor.close()
            connection.close()

            # Set the session for the newly registered user
            session["name"] = username

            response_data = {'success': True, 'message': 'Registration successful. You will be redirected in a few seconds.'}
            return render_template("profile/login_redirect.html", response_data=response_data)

        except Exception as e:
            return jsonify({'success': False, 'message': 'Error registering user: {}'.format(str(e))})

    return render_template("profile/index.html")

@app.route("/profile")
def profile():
    if not session.get("name"):
        return redirect("/login")
    response_data = {'username': session["name"]}
    return render_template('profile/profile.html', response_data=response_data)

@app.route("/profile/settings")
def settings():
    if not session.get("name"):
        return redirect("/login")
    response_data = {'username': session["name"]}
    return render_template('profile/settings.html', response_data=response_data)

@app.route("/profile/settings/change_password", methods=['GET', 'POST'])
def change_password_route():
    if not session.get("name"):
        return redirect("/login")

    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password == confirm_password:
            if new_password != old_password:
                conn = connect_to_database()
                cursor = create_cursor(conn)
                change_password(cursor, session["name"], old_password, new_password)
                conn.commit()
                cursor.close()
                conn.close()
        session["name"] = ""

    return redirect("/profile/settings")

@app.route("/profile/settings/change_username", methods=['GET', 'POST'])
def change_username_route():
    if not session.get("name"):
        return redirect("/login")

    if request.method == "POST":
        username = request.form.get('new_username')
        conn = connect_to_database()
        cursor = create_cursor(conn)
        change_username(cursor, session["name"], username)
        conn.commit()
        cursor.close()
        conn.close()
        session["name"] = ""

    return redirect("/profile/settings")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/login")

@app.route('/shirts/productpage', methods=['GET'])
def productpage():
    return render_template('shirts/productpage.html')

if __name__ == '__main__':
    app.run(debug=True)
