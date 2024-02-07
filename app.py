from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/about')
def about() -> str:
    app.logger.info("Displaying about us page")
    return render_template("about.html")


@app.route('/login')
def login_home() -> str:
    app.logger.info("Rendering login form")
    return render_template("profile/index.html")


@app.route('/login/submit', methods=['POST'])
def login_submit() -> str:
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    street = request.form.get("street")
    city = request.form.get("city")
    postal_code = request.form.get("postal_code")
    password = request.form.get("password")
    birth_date = request.form.get("birth_date")

    print('Hello')
    return f'{first_name}\n{last_name}\n{email}\n{phone}\n{street}\n{city}\n{postal_code}\n{password}\n{birth_date}'

# @app.route("/submit", methods=["POST"])
# def login_submit() -> str:



if __name__ == '__main__':
    app.run()
