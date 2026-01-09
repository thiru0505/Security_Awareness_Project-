from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd))
        data = cur.fetchone()

        if data:
            session["user"] = user
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES (NULL,?,?,?)",
                    (request.form["username"], request.form["password"], "user"))
        db.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/training")
def training():
    return render_template("training.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

app.run(debug=True)