# app.py
from flask import Flask, render_template, jsonify
import sqlite3
import random

app = Flask(__name__)

def fetch_random_image():
    conn = sqlite3.connect('image_database.db')
    cursor = conn.cursor()

    # Fetch a random image
    cursor.execute('SELECT * FROM images ORDER BY RANDOM() LIMIT 1')
    row = cursor.fetchone()

    conn.close()

    return row

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/random_image', methods=['GET'])
def get_random_image():
    image = fetch_random_image()
    return jsonify({'image': image})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

