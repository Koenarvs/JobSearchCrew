import os
import sys  # Import the sys module for handling command-line arguments

from dotenv import load_dotenv
load_dotenv()

from utils import log_agent_output
from crewai import Crew
from tasks import JobSearchTasks
from agents import JobSearchAgents
from crewai_tools import SerperDevTool

# Set the environment variables
try:
    api_base = os.environ["OPENAI_API_BASE"]
    model_name = os.environ["OPENAI_MODEL_NAME"]
    api_key = os.environ["OPENAI_API_KEY"]
    serper_api_key = os.environ["SERPER_API_KEY"]
except KeyError as e:
    log_agent_output(str(e), "Environment Variable Error")
    print(f"Error: {e}. Please set the required environment variables.")
    exit()

# Initialize necessary tools
search_tool = SerperDevTool()
tasks = JobSearchTasks()
agents = JobSearchAgents(search_tool)

print("## Welcome to the Job Search Crew")
print('-------------------------------')

# Check if the file path is provided as a command-line argument
if len(sys.argv) > 1:
    resume_path = sys.argv[1]
else:
    print("No file path provided as a command-line argument.")
    exit()

# Open the resume file and read its content
with open(resume_path, 'r') as file:
    resume_text = file.read()

# Create Agents
try:
    resume_analyzer_agent = agents.resume_analyzer_agent()
    job_searcher_agent = agents.job_searcher_agent()
    job_matcher_agent = agents.job_matcher_agent()
    report_writer_agent = agents.report_writer_agent()
except Exception as e:
    log_agent_output(str(e), "Agent Creation Error")
    print(f"Error: {e}. Failed to create agents.")
    exit()

# Create Tasks
try:
    analyze_resume_task = tasks.analyze_resume_task(resume_analyzer_agent, resume_text)
    search_jobs_task = tasks.search_jobs_task(job_searcher_agent)
    match_jobs_task = tasks.match_jobs_task(job_matcher_agent)
    write_report_task = tasks.write_report_task(report_writer_agent)
except Exception as e:
    log_agent_output(str(e), "Task Creation Error")
    print(f"Error: {e}. Failed to create tasks.")
    exit()

# Create Crew
try:
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
except Exception as e:
    log_agent_output(str(e), "Crew Creation Error")
    print(f"Error: {e}. Failed to create Crew instance.")
    exit()

result = crew.kickoff()

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Set the file path to the project folder
file_path = os.path.join(script_dir, "job_application_report.txt")

# Save the job application report to a file on the desktop
try:
    with open(file_path, 'a') as file:
        file.write(result + '\n\n')
except Exception as e:
    log_agent_output(str(e), "File Write Error")
    print(f"Error: {e}. Failed to write the job application report to the file.")
else:
    print(f"The job application report has been appended to: {file_path}")