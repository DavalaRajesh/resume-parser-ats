from sqlalchemy import or_
import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    send_from_directory,
    Response
)
from werkzeug.utils import secure_filename

from config import Config
from database import db
from parser import extract_text
from extractor import extract_resume_data
from models import Candidate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Upload folder (works on both local machine and Render)
UPLOAD_FOLDER = os.path.join(app.instance_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

with app.app_context():
    db.create_all()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def format_education(education):
    """
    Converts education dictionary into a string for database storage.
    """

    if not education:
        return "N/A"

    if isinstance(education, dict):
        degree = education.get("degree") or "N/A"
        institution = education.get("institution") or "N/A"
        year = education.get("year") or "N/A"

        return f"{degree} | {institution} | {year}"

    return str(education)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        flash("No file selected.")
        return redirect("/")

    file = request.files["resume"]

    if file.filename == "":
        flash("Please choose a file.")
        return redirect("/")

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)

# Ensure upload folder exists every time
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        print("Uploaded file:", filepath)

        text = extract_text(filepath)

        data = extract_resume_data(text)

        print("========== EXTRACTED DATA ==========")
        print(data)
        print("===================================")

        edu = data["education"]

        degree = edu.get("degree") if isinstance(edu, dict) else None
        institution = edu.get("institution") if isinstance(edu, dict) else None
        graduation_year = edu.get("year") if isinstance(edu, dict) else None

        if data["email"]:

            existing = Candidate.query.filter_by(
                email=data["email"]
            ).first()

            if existing:

                existing.name = data["name"] or existing.name
                existing.phone = data["phone"]
                existing.degree = degree
                existing.institution = institution
                existing.graduation_year = graduation_year
                existing.skills = ", ".join(data["skills"])
                existing.resume_file = filename

                db.session.commit()

                flash("Candidate Updated Successfully!")

                return redirect("/candidates")

        candidate = Candidate(
    name=data["name"] or "Unknown",
    email=data["email"],
    phone=data["phone"],
    degree=degree,
    institution=institution,
    graduation_year=graduation_year,
    skills=", ".join(data["skills"]),
    resume_file=filename,
)

        db.session.add(candidate)
        db.session.commit()

        flash("Resume Uploaded Successfully!")

        return redirect("/candidates")

    flash("Only PDF and DOCX files are allowed.")

    return redirect("/")


@app.route("/candidates")
def candidates():

    all_candidates = Candidate.query.order_by(
        Candidate.id.desc()
    ).all()

    total = Candidate.query.count()

    total_skills = sum(
        len(c.skills.split(","))
        for c in all_candidates
        if c.skills
    )

    return render_template(
        "candidates.html",
        candidates=all_candidates,
        total=total,
        total_skills=total_skills,
    )


@app.route("/candidate/<int:id>")
def candidate(id):

    candidate = Candidate.query.get_or_404(id)

    return render_template(
        "candidate.html",
        candidate=candidate
    )


@app.route("/delete/<int:id>")
def delete(id):

    candidate = Candidate.query.get_or_404(id)

    db.session.delete(candidate)

    db.session.commit()

    flash("Candidate Deleted Successfully!")

    return redirect("/candidates")


@app.route("/search")
def search():

    query = request.args.get("query", "")

    candidates = Candidate.query.filter(
        or_(
            Candidate.name.ilike(f"%{query}%"),
            Candidate.skills.ilike(f"%{query}%"),
            Candidate.email.ilike(f"%{query}%"),
        )
    ).all()

    return render_template(
        "candidates.html",
        candidates=candidates,
        total=Candidate.query.count(),
        total_skills=sum(
            len(c.skills.split(","))
            for c in Candidate.query.all()
            if c.skills
        ),
        query=query,
    )


@app.route("/resume/<filename>")
def resume(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


@app.route("/export")
def export():

    candidates = Candidate.query.all()

    csv_data = "ID,Name,Email,Phone,Education,Skills\n"

    for c in candidates:

        education = f"{c.degree} | {c.institution} | {c.graduation_year}"

        csv_data += (
            f'{c.id},"{c.name}","{c.email}",'
            f'"{c.phone}","{education}","{c.skills}"\n'
        )

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=candidates.csv"
        },
    )

if __name__ == "__main__":
    app.run(debug=True)