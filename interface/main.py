from flask import Flask, render_template,Response, jsonify, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/random_image')
def random_image():
    try:
        # Make a GET request to the server to fetch the random image
        response = requests.get('http://localhost:5001/api/random_image')
        response.raise_for_status()  # Raise an exception for any error response

        # Return the image file
        return Response(response.content, mimetype=response.headers['Content-Type'])

    except requests.exceptions.RequestException as e:
        print('Error fetching random image:', e)
        return jsonify({'error': 'Failed to fetch random image'})
@app.route('/api/classify_image', methods=['POST'])
def classify_image():
    try:
        print('0******************************')
        # Get the image file from the request
        image_file = request.files['image']
        image_file.save(f'./{image_file.filename}')
        with open(image_file.filename, 'rb') as image_file:
            print('2******************************')
            files = {'image': image_file}
            # Send a POST request to the classifier server
            response = requests.post('http://localhost:5002/api/classify_image', files=files)
            response.raise_for_status()  # Raise an exception for any error response
            # Print the classification result
            print(response.json())
            return jsonify(response.json())
    except Exception as e:
        print('Error classifying image:', e)
        return jsonify({'error': 'Failed to classify image'})

if __name__ == '__main__':
    app.run(debug=True)
##########################################################
def classify_illlmage(image_filename):
    try:
        # Open the image file in binary mode
        with open(image_filename, 'rb') as image_file:
            files = {'image': image_file}
            # Send a POST request to the classifier server
            response = requests.post('http://localhost:5002/api/classify_image', files=files)
            response.raise_for_status()  # Raise an exception for any error response
            # Print the classification result
            print(response.json())
    except Exception as e:
        print('Error classifying image:', e)
