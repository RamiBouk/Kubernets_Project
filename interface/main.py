from flask import Flask, render_template, send_file, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/random_image')
def random_image():
    try:
        # Make a GET request to the server to fetch the random image
        response = requests.get('http://localhost:5001/api/random_image', stream=True)
        response.raise_for_status()  # Raise an exception for any error response
        return Response(response.iter_content(chunk_size=1024), mimetype='image/jpeg')  # Stream the image data directly
    except requests.exceptions.RequestException as e:
        print('Error fetching random image:', e)
        return None

@app.route('/api/classify_image', methods=['POST'])
def classify_image():
    # Logic to classify the uploaded image
    # Access the uploaded file using request.files
    # Perform classification
    # Return the results as JSON
    return jsonify({'result': 'classification_result'})

if __name__ == '__main__':
    app.run(debug=True)
