# imports

from flask import Flask, render_template, request, redirect, session

from database import db
from models import User

from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import secure_filename

from resume_parser import extract_text
from matcher import calculate_match
from skills import find_skills
from ats_score import calculate_ats
from report import generate_report
app = Flask(__name__)

app.secret_key="resume_ai"


app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///resume.db"


db.init_app(app)


with app.app_context():

    db.create_all()



# HOME

@app.route("/")
def home():

    return redirect("/login")



# LOGIN ROUTE

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]

        password=request.form["password"]


        user=User.query.filter_by(
            email=email
        ).first()


        if user and check_password_hash(
            user.password,
            password
        ):

            session["user"]=user.name

            return redirect("/dashboard")


    return render_template("login.html")



# DASHBOARD

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        name=session["user"]
    )



# UPLOAD ROUTE

# UPLOAD ROUTE

@app.route("/upload", methods=["GET","POST"])
def upload():
    print("UPLOAD ROUTE ENTERED")
    
    if request.method=="POST":
        print("POST REQUEST RECEIVED")
        job=request.form["description"]

        files=request.files.getlist("resumes")
        print("FILES:", files)
        results=[]


        for file in files:

            filename=secure_filename(
                file.filename
            )


            path="uploads/"+filename


            file.save(path)


            resume_text=extract_text(path)


            score=calculate_match(
                resume_text,
                job
            )


            resume_skills=find_skills(
                resume_text
            )


            job_skills=find_skills(
                job
            )


            matched=list(
                set(resume_skills)
                &
                set(job_skills)
            )


            missing=list(
                set(job_skills)
                -
                set(resume_skills)
            )


            ats=calculate_ats(
                score,
                matched
            )

            print("RESULT:", filename, score, matched)

            results.append(
                {
                    "name": filename,
                    "score": score,
                    "ats": ats,
                    "matched": matched,
                    "missing": missing
                }
            )

            results = sorted(results, key=lambda x: x["ats"], reverse=True)

            return render_template(
    "result.html",
    results=results
)
            return render_template(
            "result.html",
            results=results
        )


    return render_template("upload.html")

@app.route("/signup", methods=["GET","POST"])
def signup():

    if request.method=="POST":

        name=request.form["name"]
        email=request.form["email"]
        password=request.form["password"]

        hashed=generate_password_hash(password)

        user=User(
            name=name,
            email=email,
            password=hashed
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")
    generate_report(results)
    return render_template("signup.html")

if __name__=="__main__":

    app.run(debug=True)