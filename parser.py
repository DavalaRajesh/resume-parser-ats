import pdfplumber
from docx import Document


def extract_text(filepath):
    # PDF
    if filepath.endswith(".pdf"):
        text = ""

        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    # DOCX
    elif filepath.endswith(".docx"):
        doc = Document(filepath)

        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text

    return ""