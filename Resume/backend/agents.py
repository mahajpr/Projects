from crewai import Agent, LLM
from tools import load_resume, extract_chunks, semantic_search
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

resume_agent = Agent(
    role="Resume Analyzer",
    goal="Understand the resume and extract relevant information",
    backstory="Expert HR analyst that evaluates candidate resumes.",
    tools=[],
    verbose=True,
    allow_delegation=False,
    llm=llm
)

job_agent = Agent(
    role="Job Requirement Analyzer",
    goal="Understand job requirements and key skills needed",
    backstory="HR expert that analyzes job descriptions.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

match_agent = Agent(
    role="Resume Matcher",
    goal="Compare resume with job description and evaluate match",
    backstory="Expert recruiter that compares resumes with job roles.",
    tools=[],
    verbose=True,
    allow_delegation=False,
    llm=llm
)






