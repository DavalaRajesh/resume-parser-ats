from database import db

class Candidate(db.Model):

    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(150), unique=True)

    phone = db.Column(db.String(30))

    degree = db.Column(db.String(200))

    institution = db.Column(db.String(250))

    graduation_year = db.Column(db.String(20))

    skills = db.Column(db.Text)

    resume_file = db.Column(db.String(255))