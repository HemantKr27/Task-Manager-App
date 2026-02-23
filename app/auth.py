from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from flask_login import login_user, login_required, logout_user
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth",__name__)


@auth.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        #checking if user already exist
        existing_user = User.query.filter_by(username = username).first()
        existing_email = User.query.filter_by(email = email).first()
        if existing_user:
            flash("Username already taken", "danger")
            return redirect(url_for("auth.register"))
        elif existing_email:
            flash("Email already registered.","danger")
            return redirect(url_for("auth.register"))
        
        #hash password
        hashed_password = generate_password_hash(password)

        #create new user
        new_user = User ( username = username,
                         email = email,
                         password = hashed_password
                         )
        
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email = email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))