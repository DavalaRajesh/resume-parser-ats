from parser import extract_text
from extractor import extract_resume_data

filepath = "uploads/Resume_Rajesh.pdf"

text = extract_text(filepath)

data = extract_resume_data(text)

print(data)