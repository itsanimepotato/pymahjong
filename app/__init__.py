from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.secret_key = "sussy key"

socketio = SocketIO(app)

import sqlite3
import data_setup
DB_FILE = "data.db"

from werkzeug.security import generate_password_hash, check_password_hash

data_setup.create_users_table()
data_setup.create_games_table()


@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return redirect(url_for('login'))

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", invalid="Invalid username or password")

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users(username,password,bio) VALUES (?,?,?)",(username,password,"No Bio"))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", invalid="Username already exists")

        conn.close()

        session["user"] = username
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/game/<int:game_id>/<int:player_id>")
def game(game_id, player_id):
    return render_template("game.html")



if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
