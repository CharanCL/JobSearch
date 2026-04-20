
import pdfplumber

def extract_resume_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

if __name__ == "__main__":
    print(extract_resume_text(
    r"C:\GITHUB\JobSearch\resume.pdf"))


