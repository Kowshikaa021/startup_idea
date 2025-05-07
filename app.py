# app.py
from flask import Flask, render_template, request
from evaluator import evaluate_idea
from dotenv import load_dotenv
import os
import shutil

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
            with open(file_path, 'r') as f:
                idea_text += "\n" + f.read()

        result = evaluate_idea(idea_text)

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)