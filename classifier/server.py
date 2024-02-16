# server.py
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'upload_folder'  # Replace with the actual path to your upload folder
CLASSIFIER_URL = 'http://classifier:5002/api/classify_image'  # Use the appropriate URL for your classifier service

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    # Remove database-related code
    return jsonify({'error': 'This endpoint is not used for image classification.'}), 400

@app.route('/api/upload_and_classify', methods=['POST'])
def upload_and_classify():
    # Check if the POST request has a file part
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']

    # If the user does not select a file, the browser may submit an empty file without a filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Forward the image to the classifier service
        try:
            response = requests.post(CLASSIFIER_URL, files={'image': open(filepath, 'rb')})
            classification_result = response.json()
            os.remove(filepath)  # Remove the uploaded image after classification
            return jsonify(classification_result)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Error communicating with the classifier service: {str(e)}'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

