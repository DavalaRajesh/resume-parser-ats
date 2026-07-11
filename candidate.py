from database import db


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(30))

    education = db.Column(db.Text)

    # Store skills as comma-separated text
    skills = db.Column(db.Text)

    resume_file = db.Column(db.String(255))

    def __repr__(self):
        return f"<Candidate {self.name}>"