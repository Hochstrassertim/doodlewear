from flask import Flask, request, render_template, redirect, session
from flask_session import Session
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def read_db_config(filename='assets/db_config.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()
        config = {line.split('=')[0].strip(): line.split('=')[1].strip() for line in lines}
    return config

def connect_to_database():
    db_config = read_db_config()
    conn = psycopg2.connect(
        dbname=db_config['dbname'],
        user=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port']
    )
    return conn

def create_cursor(conn):
    return conn.cursor()

def get_user_info(cursor, username):
    query = sql.SQL("SELECT * FROM user WHERE name = {}")
    cursor.execute(query.format(sql.Literal(username)))
    result = cursor.fetchone()
    if result:
        columns = ['username', 'password', 'role']
        return dict(zip(columns, result))
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
        user_info = get_user_info(cursor, username)
        cursor.close()
        connection.close()

        if user_info:
            if password == user_info['password']:
                session["name"] = username
                return redirect("/profile")
            else:
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

@app.route('/shirts/italy')
def italy():
    return render_template('shirts/italien.html')

if __name__ == '__main__':
    app.run(debug=True)
