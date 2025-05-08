from flask import Flask, render_template, request
from evaluator import evaluate_idea
from dotenv import load_dotenv
import os
import shutil
from PyPDF2 import PdfReader
from docx import Document

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        idea_text = request.form.get('idea_text', '')
        file = request.files.get('file')

        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Check if the uploaded file is a PDF
            if file.filename.endswith('.pdf'):
                try:
                    with open(file_path, 'rb') as f:
                        reader = PdfReader(f)
                        for page in reader.pages:
                            idea_text += page.extract_text()  # Extract text from PDF
                except Exception as e:
                    result = f"Error reading PDF file: {e}"

            # Check if the uploaded file is a DOCX
            elif file.filename.endswith('.docx'):
                try:
                    doc = Document(file_path)
                    for para in doc.paragraphs:
                        idea_text += para.text  # Extract text from DOCX
                except Exception as e:
                    result = f"Error reading DOCX file: {e}"

            # Handle text files
            elif file.filename.endswith('.txt'):
                try:
                    # Try reading the file with multiple encodings to handle charset issues
                    with open(file_path, 'r', encoding='utf-8') as f:
                        idea_text += "\n" + f.read()
                except UnicodeDecodeError:
                    try:
                        # Try ISO-8859-1 encoding if UTF-8 fails
                        with open(file_path, 'r', encoding='ISO-8859-1') as f:
                            idea_text += "\n" + f.read()
                    except UnicodeDecodeError:
                        result = "Error: Unable to read the text file. It might have an unsupported encoding."
                except Exception as e:
                    result = f"Error reading text file: {e}"

            # Handle other types of files (images, etc.)
            else:
                result = "Unsupported file type. Please upload a PDF, DOCX, or text file."

        # If there's no file, use the idea text input
        if idea_text:
            result = evaluate_idea(idea_text)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
