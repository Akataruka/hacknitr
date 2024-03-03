# Filename - server.py

# Import flask and datetime module for showing date and time
from flask import Flask, request, jsonify

# MLP for Pima Indians Dataset Serialize to JSON and HDF5
from tensorflow.keras.models import  model_from_json
from tensorflow.keras.preprocessing import image
from PIL import Image
import os
import numpy as np
import pickle as pkl

json_file = open('E:\\hacknitr\\model.json', 'r')
model_json = json_file.read()
json_file.close() 
model = model_from_json(model_json)
model.load_weights("E:\\hacknitr\\model.h5")

class_mapping = {4: ('nv', ' melanocytic nevi'), 6: ('mel', 'melanoma'), 2 :('bkl', 'benign keratosis-like lesions'), 1:('bcc' , ' basal cell carcinoma'), 5: ('vasc', ' pyogenic granulomas and hemorrhage'), 0: ('akiec', 'Actinic keratoses and intraepithelial carcinomae'),  3: ('df', 'dermatofibroma')}

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

def load_and_preprocess_image(image_path):
    img = Image.open(image_path)  # Use Image module from PIL
    img = img.resize((28, 28))  # Resize the image
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize the pixel values to be between 0 and 1
    return img_array.resize(1,28,28,3)


# Initializing flask app
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image file from the POST request
        file = request.files['image']

        # Save the image to a temporary file
        temp_path = './download.jpeg'
        file.save(temp_path)

        # Load and preprocess the image for prediction
        img_array = load_and_preprocess_image(temp_path)

        # Make predictions using the model
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions, axis=1)[0]
        class_label = list(class_mapping.keys())[list(class_mapping.values()).index(predicted_class)]

        # Remove the temporary image file
        os.remove(temp_path)

        # Return the predicted class name
        return jsonify({'class_name': class_label})

    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '_main_':
    app.run(debug=True)