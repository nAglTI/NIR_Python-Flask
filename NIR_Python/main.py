import json

from flask import Flask, redirect, session
from flask import render_template
from flask import request
from sqlalchemy import exists

from db.Connection import Connection

app = Flask(__name__, template_folder='res/templates')
conn = Connection()
with open("res/db.json") as secret_file:
    secret = json.load(secret_file)

app.secret_key = secret["flask_secret_key"]


@app.route('/')
def auth():
    return render_template("html/auth.html")


@app.route('/registration')
def reg():
    return render_template("html/reg.html")


@app.route('/feeds')
def feeds():
    if "cook" not in session:
        return redirect("/")
    db_session = conn.session()
    mess = db_session.query(conn.Message.text, conn.User.login).join(conn.User)

    return render_template("html/feeds.html", messages=[x for x in mess])


@app.route('/on_login', methods=["POST"])
def on_login():
    login = request.form.get("login")
    password = request.form.get("pass")
    db_session = conn.session()
    user = db_session.query(conn.User).filter(conn.User.login == login,
                                              conn.User.password == password).first()

    if user is None:
        return redirect("/?error=1")

    session["cook"] = user.user_id
    return redirect("/feeds")


@app.route('/on_registration', methods=["POST"])
def on_registration():
    login = request.form.get("login")
    password = request.form.get("pass")
    db_session = conn.session()

    if db_session.query(exists().where(conn.User.login == login)).scalar():
        return redirect("/registration?error=1")

    user = conn.User(login=login, password=password)

    db_session.add(user)
    db_session.commit()

    session["cook"] = user.user_id

    return redirect("/feeds")


@app.route('/on_send_click', methods=["POST"])
def on_send_click():
    mess = request.form.get("message")

    if mess is None or len(mess) == 0:
        return redirect("/feeds")

    if "cook" not in session:
        return redirect("/")

    db_session = conn.session()
    message = conn.Message(text=mess, user_id=session["cook"])
    db_session.add(message)
    db_session.commit()

    return redirect("/feeds")


@app.route('/on_exit_click', methods=["POST"])
def on_exit_click():
    session.clear()
    return redirect("/")


app.run()
