# classifier.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'upload_folder'  # Replace with the actual path to your classifier upload folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Your image classification logic goes here

@app.route('/api/classify_image', methods=['POST'])
def classify_image():
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

        # Your image classification logic goes here
        # ...

        # Example response (replace with actual classification result)
        result = {'class': 'dog', 'confidence': 0.95}

        os.remove(filepath)  # Remove the uploaded image after classification
        return jsonify(result)
    else:
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

