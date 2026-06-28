from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from database import db
from models import User

from resume_parser import extract_text
from matcher import calculate_match
from skills import find_skills
from ats_score import calculate_ats
from report import generate_report

import os

os.makedirs("uploads", exist_ok=True)
# ---------------- APP INIT ----------------
app = Flask(__name__)
app.secret_key = "secretkey123"

# ---------------- DATABASE CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ---------------- CREATE TABLES ----------------
with app.app_context():
    db.create_all()


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user:
            return render_template("login.html", error="User not found ❌")

        if not check_password_hash(user.password, password):
            return render_template("login.html", error="Wrong password ❌")

        session["user"] = user.id
        return redirect("/dashboard")

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_pw = generate_password_hash(password)

        new_user = User(name=name, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    return render_template("signup.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- UPLOAD FOLDER ----------------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ---------------- UPLOAD ----------------
job_description = "Software Developer with Python, Flask, SQL skills"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        files = request.files.getlist("resumes")
        job = request.form.get("job")

        results = []

        os.makedirs("uploads", exist_ok=True)

        for file in files:

            if file.filename == "":
                continue

            filename = secure_filename(file.filename)

            path = os.path.join("uploads", filename)

            file.save(path)

            text = extract_text(path)

            skills = find_skills(text)
            match = calculate_match(text, job)
            ats = calculate_ats(text, skills)

            results.append({
                "name": filename,
                "match": match,
                "ats": ats,
                "skills": skills
            })

        return render_template("result.html", results=results)

    return render_template("upload.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)