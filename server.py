from flask import Flask, request, jsonify, render_template
import subprocess
import os
import logging
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Flask to serve static files from the current directory
app.static_folder = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    logging.info('Received request to run script')
    data = request.get_json()
    file_path = data['filePath']
    logging.info(f'File path received: {file_path}')

    # Set the file path to the project folder
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the stdout.log file if it doesn't exist
    stdout_file = os.path.join(script_dir, 'stdout.log')
    open(stdout_file, 'a').close()

    # Redirect STDOUT to the stdout.log file
    with open(stdout_file, 'w') as stdout_writer:
        # Run main.py with the provided file path
        result = subprocess.run(['python', 'main.py', file_path], stdout=stdout_writer, stderr=subprocess.PIPE, text=True)

    # Check if the script execution was successful
    if result.returncode == 0:
        logging.info('main.py executed successfully')
        file_path = os.path.join(script_dir, "job_application_report.txt")
        
        # Read the report text from the file
        try:
            with open(file_path, 'r') as file:
                report_text = file.read()
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return jsonify({'error': 'Report file not found'}), 404
        except Exception as e:
            logging.error(f"Error reading file: {str(e)}")
            return jsonify({'error': 'Error reading report file'}), 500
        
        # Return the report text
        return jsonify({'report': report_text})
    else:
        logging.error('Error running main.py')
        logging.error(f'Error message: {result.stderr}')
        # Return an error message
        error_message = f"Error running main.py:\n{result.stderr}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    # Run the app on 0.0.0.0 (all interfaces) and port 5000
    app.run(host='0.0.0.0', port=5000)