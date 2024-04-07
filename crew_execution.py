import logging
import os
import sys
from crewai import Crew

def execute_crew_and_generate_report(agents, tasks):
    try:
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            step_callback=lambda x: logging.info(f"Crew: {x}")
        )
        report_text = crew.kickoff()
        return report_text
    except Exception as e:
        logging.error(f"Crew Execution Error: {str(e)}")
        sys.exit("Error: Failed during crew execution.")

def save_report(report_text, filename="job_application_report.txt"):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, 'w') as file:
            file.write(report_text)
        logging.info(f"The job application report has been saved to: {file_path}")
    except Exception as e:
        logging.error(f"File Write Error: {str(e)}")
        sys.exit("Error: Failed to write the job application report to the file.")
