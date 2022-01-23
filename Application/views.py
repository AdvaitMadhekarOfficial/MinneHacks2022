from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_required, current_user
from .models import User, Mail
from . import db

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home", methods=["GET", "POST"])
def home():
  return render_template("home.html", user=current_user)

@views.route("/dash-user", methods=["GET", "POST"])
@login_required
def dash_user():
  mail_get = Mail.query.filter_by(reciepient=current_user.username).all()
  print("mail_get", mail_get)
  mail_sent = Mail.query.filter_by(author=current_user.id).all()
  print("mail_sent", mail_sent)
  return render_template("dash_user.html", user=current_user, mails_get=mail_get, mails_sent=mail_sent)

@views.route("/create-mail", methods=['GET', 'POST'])
@login_required
def create_mail():
  if request.method == "POST":
    subject = request.form.get("subject")
    text = request.form.get("text")
    reciepient = request.form.get("reciepient")

    reciepient_exists = User.query.filter_by(username=reciepient).first()
    print(reciepient_exists)

    if reciepient_exists:
      print("Success 1")
      message = Mail(subject=subject, text=text, reciepient=reciepient,author=current_user.id)
      db.session.add(message)
      db.session.commit()
      flash("Mail sent successfully!", category="success")
      return redirect(url_for('views.dash_user'))
    else:
      print("Error 1")
      flash("Reciepient Username does not exist!", category="error")
  return render_template("create_mail.html", user=current_user)



