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


# @app.route("/submit", methods=["POST"])
# def login_submit() -> str:


if __name__ == '__main__':
    app.run()
