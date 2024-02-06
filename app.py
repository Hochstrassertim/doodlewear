from flask import *

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/login')
def login_home() -> str:
    app.logger.info("Rendering login form")
    return render_template("profile/index.html")


if __name__ == '__main__':
    app.run()
