from flask import Flask, request, jsonify, send_from_directory
import sys
import io
import traceback
import os
from flask_cors import CORS  # For enabling CORS

# Create a Flask app
app = Flask(__name__, static_folder='frontend')  # Serve static files from 'frontend' folder
CORS(app)  # Enable CORS to allow frontend to communicate with backend

@app.route('/')
def index():
    # Serve index.html from the frontend folder
    return send_from_directory(os.getcwd(), 'frontend/index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    # Get the code sent by the frontend
    user_code = request.json.get('code', '')
    
    # Redirect stdout to capture the output of the executed code
    output = io.StringIO()
    sys.stdout = output
    
    try:
        # Execute the user's code
        exec(user_code)
        result = output.getvalue()  # Capture the output
        return jsonify({"output": result, "error": None})
    except Exception as e:
        # Capture the error if the code fails
        error_message = traceback.format_exc()
        return jsonify({"output": None, "error": error_message})

if __name__ == '__main__':
    # Start the Flask app
    app.run(debug=True)
