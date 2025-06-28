from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'gizli_anahtar'

# Veritabanını oluştur
def init_db():
    if not os.path.exists("users.db"):
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE users (username TEXT, password TEXT)''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    return redirect(url_for("login"))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return "Giriş başarısız"
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
