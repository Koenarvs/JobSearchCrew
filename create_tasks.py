import logging
import sys
from tasks import JobSearchTasks  # Adjust existing `tasks.py` to import this function

def create_tasks(agents, resume_text):
    try:
        tasks = JobSearchTasks()
        return tasks.analyze_resume_task(agents[0], resume_text), tasks.search_jobs_task(agents[1]), tasks.match_jobs_task(agents[2]), tasks.write_report_task(agents[3])
    except Exception as e:
        logging.error(f"Task Creation Error: {str(e)}")
        sys.exit("Error: Failed to create tasks.")
