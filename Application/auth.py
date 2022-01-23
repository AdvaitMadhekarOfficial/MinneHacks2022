from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
from flask_mail import Mail, Message

auth = Blueprint("auth", __name__)

"""
def random_code():
  random_value = ""
  val_list = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
  random_value = val_list[0] + val_list[1] + val_list[2] + val_list[3] + val_list[4] + val_list[5]
  return random_value
"""
@auth.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
      if user.role == True:
        print("email is", email)
        print("password is ", password)
        print("user.password is ", user.password)
        print("CHECK:", check_password_hash(user.password, password))
        if check_password_hash(user.password, password):
          flash("Success Login!", category="success")
          login_user(user, remember=True)
          return redirect(url_for("views.dash_user"))
        else:
          flash("Password is incorrect!", category="error")
      else:
        if check_password_hash(user.password, password):
          login_user(user, remember=True)
          return redirect(url_for("views.dash_admin"))
        else:
          flash("Password is incorrect!", category="error")
    else:
      flash("This email does not exist in our database. Please create an account!", category="error")
  return render_template("login.html", user=current_user)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username")
    passwordI = request.form.get("password1")
    passwordC = request.form.get("password2")

    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()

    if email_exists:
      flash("Email exists!", category="error")
    elif username_exists:
      flash("Username exists!", category='error')
    elif passwordI != passwordC:
      flash("Passwords don't match!", category='error')
    elif len(username) < 4:
      flash("Username must be atleast 4 characters long!", category='error')
    elif len(passwordI) < 4:
      flash("Password must be atleast 4 characters long!", category='error')
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(passwordI, method='sha256'), role=True)
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash("User created!")
      return redirect(url_for("views.dash_user"))
  return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("views.home"))