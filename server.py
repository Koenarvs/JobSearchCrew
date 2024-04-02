from flask import Flask, request, jsonify, render_template
import subprocess
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Flask to serve static files from the current directory
app.static_folder = '.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        logging.info('Received request to run script')
        data = request.get_json()
        file_path = data['filePath']
        logging.info(f'File path received: {file_path}')
    except Exception as e:
        logging.error(f"Error running the script: {str(e)}")
        return jsonify({'error': 'An error occurred while running the script.'}), 500

    # Run main.py with the provided file path
    result = subprocess.run(['python', 'main.py', file_path], capture_output=True, text=True)

    # Check if the script execution was successful
    if result.returncode == 0:
        logging.info('main.py executed successfully')
        # Get the current script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the file path to the project folder
        report_path = os.path.join(script_dir, 'job_application_report.txt')
        with open(report_path, 'r', encoding='utf-8') as file:
            report_content = file.read()
            report_content = report_content.encode('utf-8', 'replace').decode('utf-8')
        # Return only the report content
        return jsonify({'report': report_content})
    else:
        logging.error('Error running main.py')
        logging.error(f'Error message: {result.stderr}')
        # Return an error message
        error_message = f"Error running main.py:\n{result.stderr}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run()