from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///registrants.db")

SPORTS = ["Basketball", "Soccer", "Ultimate Frisbee"]

REGISTRANTS = {}

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.route("/",)
def index():
    return render_template("register.html", sports=SPORTS)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        sport = request.form.get("sport")
        if not name or not sport in SPORTS:
            return "Invalid!!"
        else:
            db.execute("INSERT INTO registrants(name, sports) VALUES(?, ?)", name, sport)
            
        return redirect("/list")
    
    return redirect("/")
    

@app.route("/list")
def list():
    rows = db.execute("SELECT * FROM registrants")
    return render_template("list.html", registrants=rows)

@app.route("/deregister", methods=["POST"])
def deregister():
    if request.form.get("id"):
        try:
            db.execute("DELETE FROM registrants WHERE id = ?", request.form.get("id"))
        except TypeError:
            return "No data with the id found!!"
    else:
        return "Invalid!!"
    
    return redirect("/list")

@app.route("/update", methods=["Post"])
def update():
    if request.form.get("id"):
        try:
            data = db.execute("SELECT * FROM registrants WHERE id = ?", request.form.get("id"))
        except TypeError:
            return "No data with the id found!!"
    else:
        return "Invalid!!"
    
    return render_template("update.html", data=data[0], sports=SPORTS)

@app.route("/updatedata", methods=["POST"])
def updatedata():
    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        sport = request.form.get("sport")
        if not id or not name or not sport in SPORTS:
            return "Invalid!!"
        else:
            db.execute("UPDATE registrants SET name = ?, sports = ? WHERE id = ?", name, sport, id)
            return redirect("/list")

    return redirect("/")
