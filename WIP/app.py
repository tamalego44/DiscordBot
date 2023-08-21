from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
basicAuth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin1") #FIXME bad
}

@app.route('/')
@basicAuth.login_required
def index():
    return "Hello, %s!" % basicAuth.current_user()

@app.route("/db")
@basicAuth.login_required
def view_db():
    with open("db.csv") as fp:
        data = fp.read()
    return "<p>%s</p>" % data

@basicAuth.verify_password
def verify_password(username, password):
    if username in users and \
    check_password_hash(users.get(username), password):
        return username
