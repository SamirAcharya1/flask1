from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=["POST"])
def login():
    if not request.form.get("usr") or not request.form.get("pwd"):
        return "failure"
    else:
        user = request.form.get("usr")
        password = request.form.get("pwd")
        return "Username is " + user + " and password is " + password

@app.route("/signup", methods=["POST"])
def signup():
    if not request.form.get("usr") or not request.form.get("email") or not request.form.get("pwd"):
        return "failure"
    else:
        user = request.form.get("usr")
        email = request.form.get("email")
        password = request.form.get("pwd")
        return "username is " + user + ", email is " + email + " and password is " + password