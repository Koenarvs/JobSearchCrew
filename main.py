import sys
import logging
from dotenv import load_dotenv
load_dotenv()  # Load environment variables at the very beginning

from config import load_configuration
from log_setup import setup_logging
from initialize_agents import initialize_agents
from create_tasks import create_tasks
from crew_execution import execute_crew_and_generate_report, save_report
from crewai_tools import SerperDevTool  # Adjust based on actual module path

def main():
    # Determine if the application runs in debug mode based on command-line arguments
    debug_mode = "debug" in sys.argv
    setup_logging(debug_mode=debug_mode)

    config = load_configuration()
    search_tool = SerperDevTool(api_key=config["SERPER_API_KEY"])
    agents = initialize_agents(search_tool)

    if len(sys.argv) > 1 and sys.argv[-1] != "debug":
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
