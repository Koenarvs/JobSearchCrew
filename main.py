import os
from dotenv import load_dotenv

load_dotenv()

from utils import log_agent_output
from crewai import Crew
from tasks import JobSearchTasks
from agents import JobSearchAgents
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# Set the environment variables
os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4-turbo-preview"

# Retrieve the environment variables
api_base = os.environ["OPENAI_API_BASE"]
model_name = os.environ["OPENAI_MODEL_NAME"]
api_key = os.environ["OPENAI_API_KEY"]

# Set the Serper API key
os.environ["SERPER_API_KEY"] = "1ac524b3dbc9d62548e9225fd093fd3a735b25bd"

# Initialize necessary tools
search_tool = SerperDevTool()

tasks = JobSearchTasks()
agents = JobSearchAgents(search_tool)

print("## Welcome to the Job Search Crew")
print('-------------------------------')
resume_path = input("Enter the path to your resume file: ")
resume_path = resume_path.strip('"')

with open(resume_path, 'r') as file:
    resume_text = file.read()

# Create Agents
resume_analyzer_agent = agents.resume_analyzer_agent()
job_searcher_agent = agents.job_searcher_agent()
job_matcher_agent = agents.job_matcher_agent()
report_writer_agent = agents.report_writer_agent()

# Create Tasks
analyze_resume_task = tasks.analyze_resume_task(resume_analyzer_agent, resume_text)
search_jobs_task = tasks.search_jobs_task(job_searcher_agent)
match_jobs_task = tasks.match_jobs_task(job_matcher_agent)
write_report_task = tasks.write_report_task(report_writer_agent)
# Create Crew
crew = Crew(
    agents=[
        resume_analyzer_agent,
        job_searcher_agent,
        job_matcher_agent,
        report_writer_agent
    ],
    tasks=[
        analyze_resume_task,
        search_jobs_task,
        match_jobs_task,
        write_report_task
    ],
    verbose=True,
    step_callback=lambda x: log_agent_output(x, "Crew")
)

result = crew.kickoff()

# Save the job application report to a file on the desktop
desktop_path = os.path.expanduser("~/Desktop")
file_path = os.path.join(desktop_path, "job_application_report.txt")
with open(file_path, 'a') as file:
    file.write(result + '\n\n')  # Add newline characters for separation

print(f"The job application report has been appended to: {file_path}")
