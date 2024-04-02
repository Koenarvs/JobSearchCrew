from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_script', methods=['POST'])
def run_script():
    data = request.get_json()
    file_path = data['filePath']

    # Run main.py with the provided file path
    result = subprocess.run(['python', 'main.py', file_path], capture_output=True, text=True)

    # Check if the script execution was successful
    if result.returncode == 0:
        # Return the output of main.py
        return result.stdout
    else:
        # Return an error message
        error_message = f"Error running main.py:\n{result.stderr}"
        return jsonify({'error': error_message}), 500

if __name__ == '__main__':
    app.run()