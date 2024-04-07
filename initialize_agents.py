import logging
import sys
from agents import JobSearchAgents  # Assuming `agents.py` exists and is in the same directory

def initialize_agents(search_tool):
    try:
        agents = JobSearchAgents(search_tool)
        return agents.resume_analyzer_agent(), agents.job_searcher_agent(), agents.job_matcher_agent(), agents.report_writer_agent()
    except Exception as e:
        logging.error(f"Agent Creation Error: {str(e)}")
        sys.exit("Error: Failed to create agents.")
