import os

class Config:

    SECRET_KEY = "resume-parser"

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:0957@localhost:9057/resume_parser"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"