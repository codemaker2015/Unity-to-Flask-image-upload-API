from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
from werkzeug.utils import secure_filename  # For secure filenames

app = Flask(__name__)

# Enable CORS for all routes and origins
CORS(app)

# Define the upload folder (project root)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the request has the 'file' part
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Check if a file is selected
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    # Validate the file type
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    try:
        # Secure the filename and save it
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return jsonify({
            "message": "File successfully uploaded",
            "file_path": file_path
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask server on all interfaces (0.0.0.0) to allow outside access
    app.run(host='0.0.0.0', port=5000, debug=True)
