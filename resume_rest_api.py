import os
import tempfile
import PyPDF2
from pyresparser import ResumeParser
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/resume_parser", methods=["POST"])
def resume_parser():
    if "resume" not in request.files:
        return jsonify({"error": "No file found."}), 400

    resume = request.files["resume"]
    if (
        not resume.filename.endswith(".doc")
        and not resume.filename.endswith(".docx")
        and not resume.filename.endswith(".pdf")
    ):
        return (
            jsonify(
                {
                    "error": "Invalid file type. Only .doc, .docx, and .pdf files are supported."
                }
            ),
            400,
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(resume.read())
        temp.flush()
        data = ResumeParser(temp.name).get_extracted_data()
        print(data["skills"])
        matching_skills = request.form.get("matching_skills").lower().split(",")
        data_skills = [skill.lower() for skill in data["skills"]]
        matching_skills = list(set(matching_skills) & set(data_skills))
        if matching_skills:
            message = "Match found with skills"
        else:
            message = "No match found with skills"

    os.unlink(temp.name)
    return (
        jsonify({"message": message, "matching_skills": matching_skills, "data": data}),
        200,
    )

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error."}), 500

if __name__ == "__main__":
    app.run(debug=True)
