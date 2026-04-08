from crewai import Crew
from agents import resume_agent, job_agent, match_agent
from tasks import resume_task, job_task, match_task

crew = Crew(
    agents=[resume_agent, job_agent, match_agent],
    tasks=[resume_task, job_task, match_task],
    verbose=True
)