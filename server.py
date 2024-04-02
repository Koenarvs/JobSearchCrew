from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__)

# Configure Flask to serve static files from the current directory
app.static_folder = '.'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.get_json()
    file_path = data['filePath']
    # Run main.py with the provided file path
    result = subprocess.run(['python', 'main.py', file_path], capture_output=True, text=True)
    # Check if the script execution was successful
    if result.returncode == 0:
        # Read the contents of job_application_report.txt
        script_dir = os.path.dirname(os.path.abspath(__file__))
        report_path = os.path.join(script_dir, 'job_application_report.txt')
        with open(report_path, 'r') as file:
            report_content = file.read()
        # Return the output of main.py and the report content
        return jsonify({'output': result.stdout, 'report': report_content})
    else:
        # Return an error message
        error_message = f"Error running main.py:\n{result.stderr}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run()