import sys
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Immediate log to test early script execution
logging.basicConfig(level=logging.DEBUG)
logging.debug("Starting script execution.")

load_dotenv(verbose=True)  # Load environment variables at the very beginning

from config import load_configuration
from log_setup import setup_logging
from initialize_agents import initialize_agents
from create_tasks import create_tasks
from crew_execution import execute_crew_and_generate_report, save_report
from crewai_tools import SerperDevTool  # Adjust based on actual module path
#from google_jobs_api_tool import GoogleJobsAPITool

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def main():
    # Determine if the application runs in debug mode based on command-line arguments
    debug_mode = "debug" in sys.argv
    setup_logging(debug_mode=debug_mode)

    config = load_configuration()
    search_tool = SerperDevTool(api_key=config["SERPER_API_KEY"])
    #search_tool = GoogleJobsAPITool()
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

# New API endpoint for uploading resume
@app.route('/api/upload_resume', methods=['POST'])
def upload_resume():
    file_path = request.json.get('file_path')
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    try:
        with open(file_path, 'r') as file:
            resume_text = file.read()
        
        # Initialize agents and create tasks
        config = load_configuration()
        search_tool = SerperDevTool(api_key=config["SERPER_API_KEY"])
        agents = initialize_agents(search_tool)
        tasks = create_tasks(agents, resume_text)

        # Execute crew and generate report
        report_text = execute_crew_and_generate_report(agents, tasks)
        save_report(report_text)

        return jsonify({"message": "Resume processed successfully"}), 200
    except IOError as e:
        logging.error(f"Error reading resume file {file_path}: {e}")
        return jsonify({"error": "Failed to read resume file"}), 500
    except Exception as e:
        logging.error(f"Error processing resume: {e}")
        return jsonify({"error": "Failed to process resume"}), 500

# New API endpoint for fetching job matches
@app.route('/api/job_matches', methods=['GET'])
def job_matches():
    try:
        # TODO: Implement logic to fetch actual job matches
        # For now, return dummy data
        matches = [
            {"id": 1, "title": "Software Developer", "company": "Tech Co"},
            {"id": 2, "title": "Data Analyst", "company": "Data Corp"},
        ]
        return jsonify(matches), 200
    except Exception as e:
        logging.error(f"Error fetching job matches: {e}")
        return jsonify({"error": "Failed to fetch job matches"}), 500

if __name__ == "__main__":
    # Check if we're running in API mode or script mode
    if "--api" in sys.argv:
        # Run in API mode
        debug_mode = "debug" in sys.argv
        app.run(debug=debug_mode)
    else:
        # Run in script mode
        main()