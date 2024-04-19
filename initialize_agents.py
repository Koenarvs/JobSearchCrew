import logging
import sys
from agents import JobSearchAgents  # Ensure this matches the actual class name and file

def initialize_agents(search_tool):
    try:
        job_search_agents = JobSearchAgents(search_tool)
        return (
            job_search_agents.resume_analyzer_agent(),
            job_search_agents.job_searcher_agent(),
            job_search_agents.job_matcher_agent(),
            job_search_agents.report_writer_agent()
        )
    except Exception as e:
        logging.error(f"Agent Creation Error: {str(e)}")
        sys.exit("Error: Failed to create agents.")
