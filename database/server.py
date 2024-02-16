# server.py
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import os
import random
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE_PATH = 'image_database.db'
IMAGE_FOLDER = ''  # Replace with the actual path to your image folder

def fetch_random_image_path():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Fetch a random image path
    cursor.execute('SELECT filepath FROM images ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]
    else:
        return None

@app.route('/api/random_image', methods=['GET'])
def get_random_image():
    image_path = fetch_random_image_path()

    if image_path:
        # Construct the full path to the image
        full_path =  image_path

        # Send the image file in the response
        return send_file(full_path, mimetype='image/jpeg')
    else:
        return jsonify({'error': 'No images available'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

