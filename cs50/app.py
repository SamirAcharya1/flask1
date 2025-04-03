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
    if not request.form.get("name") or not request.form.get("sport"):
        return "Invalid!!"
    else:
        name = request.form.get("name")
        sport = request.form.get("sport")
        REGISTRANTS[name] = sport
        
    return redirect("/list")
    

@app.route("/list")
def list():
    return render_template("list.html", registrants=REGISTRANTS)

@app.route("/deregister", methods=["POST"])
def deregister():
    if request.form.get("id"):
        try:
            del REGISTRANTS[request.form.get("id")]
        except KeyError:
            return "No data with the id found!!"
    else:
        return "Invalid!!"
    
    return redirect("/list")