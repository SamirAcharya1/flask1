from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from func import generate_user_id, validEmail
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///userdata.db")

@app.route("/")
def index():
    userId = session.get("userId")
    if not userId:
        return render_template("index.html")
    else:
        try:
            username = db.execute("SELECT username FROM users WHERE id = ?", userId)
        except Exception as e:
            return "Exception"
        
        return render_template("index.html", username=username[0]["username"])

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("usr")
        password = request.form.get("pwd")
        
        if not user or not password:
            return "failure"
        elif len(password) < 8:
            return "failure"
        
        userId = generate_user_id(user)
        
        try:
            hashedPass = db.execute("SELECT password_hash FROM users WHERE id = ?", userId)
        except Exception as e:
            return "Exception"
        
        if hashedPass and check_password_hash(hashedPass[0]["password_hash"], password):
            session["userId"] = userId
            return redirect("/")
        else:
            return "Log In Failed" 
            
    
    return redirect("/")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        user = request.form.get("usr")
        email = request.form.get("email")
        password = request.form.get("pwd")
        
        if not user or not email or not password:
            return "failure"
        elif len(password) < 8:
            return "failure"
        elif not validEmail(email):
            return "email failure"
        
        userId = generate_user_id(user)
        passwordHash = generate_password_hash(password)
        
        try:
            db.execute("INSERT INTO users (id, username, email, password_hash) VALUES(?, ?, ?, ?)", userId, user, email, passwordHash)
        except Exception as e:
            return "Exception"
        
        return redirect(url_for("index", userId=userId))
    
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")