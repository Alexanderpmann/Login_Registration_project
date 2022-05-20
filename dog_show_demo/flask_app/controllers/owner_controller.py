from flask_app import app
from flask import render_template, redirect, request, session, flash

#controllers file always has upper case model name
from flask_app.models.owner import Owner 

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

# =================================================
# Register / Login Routes
# =================================================

@app.route("/register", methods=["POST"])
def register():
    # 1 - validating form information
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "pass_conf" : request.form["pass_conf"]
    }

    if not Owner.validate_register(data):
        return redirect("/")

    # 2 - bcrypt password
    data["password"] = bcrypt.generate_password_hash(request.form['password'])

    # 3 - save new owner to db
    new_owner_id = Owner.create_owner(data)
    # 4 - enter owner id into session and redirect to dashboard
    session["owner_id"] = new_owner_id
    return redirect("/dashboard")

@app.route("/login", methods=["POST"])
def login():
    # 1 - validate login info
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }
    if not Owner.validate_login(data):
        return redirect("/")
    # 2 - query for owner info based on email
    owner = Owner.get_by_email(data)

    # 3 - put owner id into session and redirect to dashboard
    session["owner_id"] = owner.id
    return redirect("/dashboard")


# =================================================
# Render Dashboard Route
# =================================================

@app.route("/dashboard")
def dashboard():
    if "owner_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    data = {
        "owner_id" : session["owner_id"]
    }

    owner = Owner.get_by_id(data)

    return render_template("dashboard.html", owner = owner)


# =================================================
# Logout Route
# =================================================

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out!")
    return redirect("/")