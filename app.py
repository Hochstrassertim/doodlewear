from flask import Flask, request, render_template, redirect, session
from flask_session import Session

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Hard-coded users (replace with database later)
users = {
    'admin': {'password': 'admin_password', 'role': 'admin'},
    'user': {'password': 'user_password', 'role': 'normal'}
}


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
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect('/profile')

        return render_template('profile/index.html', error='Invalid username or password')

    return render_template('profile/index.html', error='')


@app.route('/login_submit', methods=['POST'])
def login_submit():
    if request.method == 'POST':
        #first_name = request.form['first_name']
        #last_name = request.form['last_name']
        #email = request.form['email']
        #phone = request.form['phone']
        #street = request.form['street']
        #city = request.form['city']
        #postal_code = request.form['postal_code']
        #password = request.form['password']
        #birth_date = request.form['birth_date']
#
        ## Add your logic to insert the user into the database or perform login verification
        ## For simplicity, I'll just print the values for now
        #print(f'First Name: {first_name}')
        #print(f'Last Name: {last_name}')
        #print(f'Email: {email}')
        #print(f'Phone: {phone}')
        #print(f'Street: {street}')
        #print(f'City: {city}')
        #print(f'Postal Code: {postal_code}')
        #print(f'Password: {password}')
        #print(f'Birth Date: {birth_date}')

        session["name"] = request.form.get("name")
        # redirect to the main page
        return redirect("/login")
    return render_template("profile/index.html")

@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        user_role = users[username]['role']
        return render_template('profile.html', username=username, role=user_role)

    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
