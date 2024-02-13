# classifier.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
import numpy
import os
from PIL import Image
import pickle


app = Flask(__name__)
CORS(app)
model = tf.keras.models.load_model("models/model_1.h5")

# Load the ClassLabel object from the file
with open('class_label.pkl', 'rb') as file:
    loaded_class_label = pickle.load(file)

# Now, loaded_class_label is the ClassLabel object


UPLOAD_FOLDER = 'upload_folder'  # Replace with the actual path to your classifier upload folder

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Your image classification logic goes here
def predict(x, top_k=5):
    input_shape = model.layers[0].input_shape[1:]
    x=numpy.array(x.resize((224,224)))/255
    if tf.is_tensor(x):
        x = tf.reshape(x[0], [1] + list(input_shape))
    elif isinstance(x, numpy.ndarray):
        if x.shape[-1] != 3:
            # If the image has an alpha channel (transparency), remove it
            x = x[:, :, :3]
        assert x.shape == input_shape
        x = tf.reshape(x, [1] + list(input_shape))

    # predict
    pred = model.predict(x)
    top_k_pred, top_k_indices = tf.math.top_k(pred, k=top_k)
    # display the prediction
    predictions = dict()
    for ct in range(top_k):
        name = loaded_class_label.int2str(top_k_indices[0][ct])
        name = "".join(name.split('-')[1:])
        value = top_k_pred.numpy()[0][ct]
        predictions[name] = value
        print(name + " : {:.2f}%".format(value*100))
	
    return predictions

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
        img =Image.open(filepath)

        res=predict(img,3)

        # Example response (replace with actual classification result)
        result = {key: float(value) for key, value in res.items()}



        os.remove(filepath)  # Remove the uploaded image after classification
        return jsonify(result)
    else:
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)

