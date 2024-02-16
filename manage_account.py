
import psycopg2
import datetime
import socket
from socket import gethostname

server_hostname = "srv-cn5lbkgl5elc73e7hus0-hibernate-689d6995f9-v54tm"
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

def change_address(cursor, username, street, house_number, city, postal_code, country):
    # Check if the new username already exists (case-insensitive)
    check_query = "SELECT * FROM users WHERE LOWER(username) = LOWER(%s)"
    cursor.execute(check_query, (username.lower(),))
    existing_user = cursor.fetchone()

    #if existing_user:
    #    # New username already exists, handle accordingly (e.g., raise an exception or return an error)
    #    raise ValueError("New username already exists")

    # Update the username
    update_query = """
        UPDATE users SET (street, house_number, city, postal_code, country) = (%s, %s, %s, %s, %s) WHERE LOWER(username) = LOWER(%s)
    """
    (cursor.execute (update_query, (street, house_number, city, postal_code, country, username.lower())))

def delete_user(cursor, username):
    update_query = """
        DELETE FROM users WHERE LOWER(username) = LOWER(%s)
    """
    (cursor.execute(update_query, username))