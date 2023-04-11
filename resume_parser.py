import os
import docx2txt
from pyresparser import ResumeParser
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume = request.files['resume']
        resume.save(resume.filename)
        if resume.filename.endswith('.doc'):
            text = docx2txt.process(resume.filename)
            data = ResumeParser(text).get_extracted_data()
        else:
            data = ResumeParser(resume.filename).get_extracted_data()
        os.remove(resume.filename)
        return render_template('resume_details.html', resume=data)
    return render_template('upload_resume.html')

if __name__ == '__main__':
    app.run(debug=True)
