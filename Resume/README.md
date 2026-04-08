Resume Agent AI

AI-powered Resume Analyzer and Job Matching System built using Agentic AI architecture.
This project analyzes resumes and compares them with job descriptions to evaluate how well a candidate matches a role.

It uses multi-agent reasoning to simulate how HR teams review resumes.

Features :

Upload and analyze resumes in PDF format

Compare resume with job description

Generate AI-based match analysis

Identify matching and missing skills

Multi-agent system for intelligent reasoning

Simple UI using Streamlit

Architecture :

This project follows an Agentic AI workflow.

User Resume + Job Description
        ↓
FastAPI Backend
        ↓
CrewAI Agents
   • Resume Analyzer
   • Job Requirement Analyzer
   • Resume Matcher
        ↓
Groq LLM (Llama3)
        ↓
Match Score + Skill Analysis

Project Structure :
Resume-Agent-AI
│
├── backend
│   ├── main.py            # FastAPI backend
│   ├── agents.py          # AI agents
│   ├── tasks.py           # Agent tasks
│   ├── crew.py            # Agent orchestration
│   ├── tools.py           # Resume processing tools
│   ├── uploads/           # Uploaded resumes
│   └── Dockerfile
│
├── frontend
│   ├── streamlit.py       # Streamlit UI
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
Technologies Used :

Python

FastAPI

Streamlit

CrewAI

Groq LLM

Sentence Transformers

FAISS

Docker

Installation :

Clone the repository.

git clone https://github.com/yourusername/resume-agent-ai.git
cd resume-agent-ai

Create a virtual environment.

python -m venv venv

Activate the environment.

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

Install dependencies.

pip install -r requirements.txt
Environment Variables

Create a .env file in the project root.

GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=dummy

Run Backend
uvicorn backend.main:app --reload

Open API documentation:

http://127.0.0.1:8000/docs
Run Frontend
streamlit run frontend/streamlit.py

The UI will open at:

http://localhost:8501
Example Output
Match Score: 82%

Matching Skills
• Python
• FastAPI
• Machine Learning

Missing Skills
• Docker
• Kubernetes

Recommendation
Candidate is strong in backend development but lacks DevOps experience.
Deployment

The project can be deployed using:

Docker

Render

Railway

Streamlit Cloud (frontend only)

Example Docker run:

docker compose up --build
