import os

class Config:
    SECRET_KEY = "resume-parser"

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://resume_parser_wqqs_user:kN0dXLneYlj2AfRBIUK4QC6e8Eehv4Jm@dpg-d9can2m7r5hc73eu93og-a/resume_parser_wqqs"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"