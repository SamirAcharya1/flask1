from flask import Flask, render_template, request, redirect

app = Flask(__name__)

SPORTS = ["Basketball", "Soccer", "Ultimate Frisbee"]

REGISTRANTS = {
    
}

@app.route("/",)
def index():
    return render_template("register.html", sports=SPORTS)

@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("name"):
        return "Invalid!!"
    for sport in request.form.getlist("sport"):
        if sport not in SPORTS:
            return "Invalid!"
        else:
            name = request.form.get("name")
            REGISTRANTS[name] = request.form.getlist("sport")
    
    return redirect("/list")
    

@app.route("/list")
def list():
    return render_template("list.html", registrants=REGISTRANTS)