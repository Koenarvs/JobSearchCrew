from flask import Flask, request, jsonify, render_template
import subprocess
import os
import logging
import json

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
    logging.info('Received request to run script')
    data = request.get_json()
    file_path = data['filePath']
    logging.info(f'File path received: {file_path}')

    # Run main.py with the provided file path
    result = subprocess.run(['python', 'main.py', file_path], capture_output=True, text=True)

    # Check if the script execution was successful
    if result.returncode == 0:
        logging.info('main.py executed successfully')
        # Extract the report text from the JSON payload
        try:
            report_data = json.loads(result.stdout)
            report_text = report_data.get('report', '')
        except json.JSONDecodeError:
            logging.error('Error decoding JSON payload from main.py')
            report_text = ''
        # Return the report text
        return jsonify({'report': report_text})
    else:
        logging.error('Error running main.py')
        logging.error(f'Error message: {result.stderr}')
        # Return an error message
        error_message = f"Error running main.py:\n{result.stderr}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run()