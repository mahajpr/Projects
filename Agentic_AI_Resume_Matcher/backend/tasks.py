
from crewai import Task
from agents import resume_agent, job_agent, match_agent


resume_task = Task(
    description="""
Analyze the following resume:

{resume_text}

Extract:
- Skills
- Experience
- Key details

Do NOT use tools.
Extract key skills, experience, and important information.
""",
    agent=resume_agent,
    expected_output="Summary of candidate skills and experience"
)


job_task = Task(
    description="""
Analyze the following job description and identify
the important skills and requirements.

Job Description:
{job_desc}
""",
    agent=job_agent,
    expected_output="List of key job requirements"
)


match_task = Task(
    description="""
Compare the candidate resume with the job description.

STRICTLY return output in the following format (do not add anything else):

Match score: <percentage>

Matching skills: <comma separated skills>

Missing skills: <comma separated skills>

Final recommendation: <short paragraph>
""",
    agent=match_agent,
    expected_output="Structured match analysis"
)