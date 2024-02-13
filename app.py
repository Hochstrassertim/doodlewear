import psycopg2
import socket
from flask import Flask, request, render_template, redirect, session
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def connect_to_database():
    # Connection string for PostgreSQL

    if socket.gethostname() == "srv-cn5lbkgl5elc73e7hus0-hibernate-689d6995f9-v54tm":
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

            return render_template("profile/index.html", error="Invalid password")

        return render_template("profile/index.html", error="Invalid username")

    return render_template("profile/index.html")

@app.route('/login_submit', methods=['POST'])
def login_submit():
    if request.method == 'POST':
        session["name"] = request.form.get("name")
        return redirect("/login")
    return render_template("profile/index.html")

@app.route("/profile")
def profile():
    if not session.get("name"):
        return redirect("/login")
    return render_template('profile/profile.html')

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/login")

# Route for printing all users

@app.route('/shirts/italy')
def italy():
    return render_template('shirts/italien.html')

@app.route('/hostname')
def hostname():
    return socket.gethostname()

if __name__ == '__main__':
    app.run(debug=True)
