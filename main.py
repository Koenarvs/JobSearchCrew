import sys
import logging
from dotenv import load_dotenv
# Ensure environment variables are loaded at the very beginning
load_dotenv()

from config import load_configuration
from log_setup import setup_logging
from initialize_agents import initialize_agents
from create_tasks import create_tasks
from crew_execution import execute_crew_and_generate_report, save_report
from crewai_tools import SerperDevTool  # Adjust based on actual module path

def main():
    # Initialize debug_mode based on whether "debug" is the last argument
    debug_mode = sys.argv[-1] == "debug"

    # Setup logging with or without debug mode
    setup_logging(debug_mode=debug_mode)

    config = load_configuration()
    
    # Initialize SerperDevTool (or similar) with the necessary API key
    search_tool = SerperDevTool(api_key=config["SERPER_API_KEY"])
    
    agents = initialize_agents(search_tool)
    
    if len(sys.argv) > 1 and not debug_mode:
        # If not in debug mode, the resume path is the first argument
        resume_path = sys.argv[1]
    elif len(sys.argv) > 2 and debug_mode:
        # If in debug mode and an extra argument is provided, the resume path is the second argument
        resume_path = sys.argv[1]
    else:
        logging.error("No resume file path provided as a command-line argument.")
        sys.exit(1)
    
    try:
        with open(resume_path, 'r') as file:
            resume_text = file.read()
    except IOError as e:
        logging.error(f"Error reading resume file {resume_path}: {e}")
        sys.exit(1)

    tasks = create_tasks(agents, resume_text)
    report_text = execute_crew_and_generate_report(agents, tasks)
    save_report(report_text)

if __name__ == "__main__":
    main()
