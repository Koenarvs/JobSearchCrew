import os
import sys
import json
import logging
from dotenv import load_dotenv
load_dotenv()
from crewai import Crew
from tasks import JobSearchTasks
from agents import JobSearchAgents
from tavily import TavilyClient
from crewai_tools import SerperDevTool

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the file path for the app.log file
log_file_path = os.path.join(script_dir, 'app.log')

# Configure logging
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the environment variables
try:
    api_base = os.environ["OPENAI_API_BASE"]
    model_name = os.environ["OPENAI_MODEL_NAME"]
    api_key = os.environ["OPENAI_API_KEY"]
    serper_api_key = os.environ["SERPER_API_KEY"]
except KeyError as e:
    logging.error(f"Environment Variable Error: {str(e)}")
    logging.error("Error: Please set the required environment variables.")
    exit()

# Initialize necessary tools
search_tool = SerperDevTool()
tasks = JobSearchTasks()
agents = JobSearchAgents(search_tool)

logging.info("Welcome to the Job Search Crew")

# Check if the file path is provided as a command-line argument
if len(sys.argv) > 1:
    resume_path = sys.argv[1]
else:
    logging.error("No file path provided as a command-line argument.")
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
    logging.error(f"Agent Creation Error: {str(e)}")
    logging.error("Error: Failed to create agents.")
    exit()

# Create Tasks
try:
    analyze_resume_task = tasks.analyze_resume_task(resume_analyzer_agent, resume_text)
    search_jobs_task = tasks.search_jobs_task(job_searcher_agent)
    match_jobs_task = tasks.match_jobs_task(job_matcher_agent)
    write_report_task = tasks.write_report_task(report_writer_agent)
except Exception as e:
    logging.error(f"Task Creation Error: {str(e)}")
    logging.error("Error: Failed to create tasks.")
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
        step_callback=lambda x: logging.info(f"Crew: {x}")
    )
except Exception as e:
    logging.error(f"Crew Creation Error: {str(e)}")
    logging.error("Error: Failed to create Crew instance.")
    exit()

# Execute the Crew and get the report text
report_text = crew.kickoff()

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the file path to the project folder
file_path = os.path.join(script_dir, "job_application_report.txt")

# Save the job application report to a file
try:
    with open(file_path, 'w') as file:
        file.write(report_text)
except Exception as e:
    logging.error(f"File Write Error: {str(e)}")
    logging.error("Error: Failed to write the job application report to the file.")
else:
    logging.info(f"The job application report has been saved to: {file_path}")