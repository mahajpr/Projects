from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import os
import re
from crew import crew
import fitz

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

class Job(BaseModel):
    query: str


@app.post("/upload-resume")
def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return {
        "message": "Resume uploaded successfully",
        "file_name": file.filename
    }


@app.post("/match-resume-agent")
def match_resume_agent(file_name: str, req: Job):

    resume_path = os.path.join(UPLOAD_DIR, file_name)

    if not os.path.exists(resume_path):
        return {"error": "Resume not found"}
    
    def extract_pdf_text(path):
        text = ""
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
        return text
    
    resume_text = extract_pdf_text(resume_path)

    result = crew.kickoff(inputs={
        "resume_text": resume_text,
        "job_desc": req.query
    })

    # ✅ Extract raw text only
    raw_text = result.raw if hasattr(result, "raw") else str(result)

    # ✅ Helper function
    def extract(pattern, text):
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else "Not found"

    # ✅ Extract sections
    match_score = extract(r"Match score:\s*(.*?)\n", raw_text)
    matching_skills = extract(r"Matching skills:\s*(.*?)\n", raw_text)
    missing_skills = extract(r"Missing skills:\s*(.*?)\n", raw_text)
    final_recommendation = extract(r"Final recommendation:\s*(.*)", raw_text)

    return {
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "final_recommendation": final_recommendation
    }



