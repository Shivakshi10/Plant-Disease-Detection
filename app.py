from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import pickle





# Load model
# model_path = 'model.pkl'
# with open(model_path,'rb') as file:
#     model=pickle.load(file)
model = load_model('my_model2.keras')
#model = load_model('/backend/plant_disease_model2.h5')


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
# Replace with your class names in order
# Create a mapping from class indices to class names

# class_indices = {
#     0: 'Apple___Apple_scab',
#     1: 'Apple___Black_rot',
#     2: 'Apple___Cedar_apple_rust',
#     3: 'Apple___healthy',
#     4: 'Blueberry___healthy',
#     5: 'Cherry_(including_sour)___Powdery_mildew',
#     6: 'Cherry_(including_sour)___healthy',
#     7: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
#     8: 'Corn_(maize)___Common_rust_',
#     9: 'Corn_(maize)___Northern_Leaf_Blight',
#     10: 'Corn_(maize)___healthy',
#     11: 'Grape___Black_rot',
#     12: 'Grape___Esca_(Black_Measles)',
#     13: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
#     14: 'Grape___healthy',
#     15: 'Orange___Haunglongbing_(Citrus_greening)',
#     16: 'Peach___Bacterial_spot',
#     17: 'Peach___healthy',
#     18: 'Pepper,_bell___Bacterial_spot',
#     19: 'Pepper,_bell___healthy',
#     20: 'Potato___Early_blight',
#     21: 'Potato___Late_blight',
#     22: 'Potato___healthy',
#     23: 'Raspberry___healthy',
#     24: 'Soybean___healthy',
#     25: 'Squash___Powdery_mildew',
#     26: 'Strawberry___Leaf_scorch',
#     27: 'Strawberry___healthy',
#     28: 'Tomato___Bacterial_spot',
#     29: 'Tomato___Early_blight',
#     30: 'Tomato___Late_blight',
#     31: 'Tomato___Leaf_Mold',
#     32: 'Tomato___Septoria_leaf_spot',
#     33: 'Tomato___Spider_mites Two-spotted_spider_mite',
#     34: 'Tomato___Target_Spot',
#     35: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
#     36: 'Tomato___Tomato_mosaic_virus',
#     37: 'Tomato___healthy'
# }

# class_indices = {
#     0: 'scab',
#     1: 'Black_rot',
#     2: 'rust',
#     3: 'healthy',
#     4: 'healthy',
#     5: 'Powdery_mildew',
#     6: 'healthy',
#     7: 'Cercospora_leaf_spot Gray_leaf_spot',
#     8: 'Common_rust',
#     9: 'Northern_Leaf_Blight',
#     10: 'healthy',
#     11: 'Black_rot',
#     12: 'Esca_(Black_Measles)',
#     13: 'Leaf_blight_(Isariopsis_Leaf_Spot)',
#     14: 'healthy',
#     15: 'Haunglongbing_(Citrus_greening)',
#     16: 'Bacterial_spot',
#     17: 'healthy',
#     18: 'Bacterial_spot',
#     19: 'healthy',
#     20: 'Early_blight',
#     21: 'Late_blight',
#     22: 'healthy',
#     23: 'healthy',
#     24: 'healthy',
#     25: 'Powdery_mildew',
#     26: 'Leaf_scorch',
#     27: 'healthy',
#     28: 'Bacterial_spot',
#     29: 'Early_blight',
#     30: 'Late_blight',
#     31: 'Leaf_Mold',
#     32: 'Septoria_leaf_spot',
#     33: 'Spider_mites Two-spotted_spider_mite',
#     34: 'Target_Spot',
#     35: 'Yellow_Leaf_Curl_Virus',
#     36: 'mosaic_virus',
#     37: 'healthy'
# }

class_indices = {
    0: {"plant": "Apple", "disease": "Apple scab"},
    1: {"plant": "Apple", "disease": "Black rot"},
    2: {"plant": "Apple", "disease": "Cedar apple rust"},
    3: {"plant": "Apple", "disease": "No disease found, Healthy"},
    4: {"plant": "Blueberry", "disease": "No disease found, Healthy"},
    5: {"plant": "Cherry_(including_sour)", "disease": "Powdery mildew"},
    6: {"plant": "Cherry_(including_sour)", "disease": "No disease found, Healthy"},
    7: {"plant": "Corn_(maize)", "disease": "Cercospora leaf spot Gray leaf spot"},
    8: {"plant": "Corn_(maize)", "disease": "Common rust"},
    9: {"plant": "Corn_(maize)", "disease": "Northern Leaf Blight"},
    10: {"plant": "Corn_(maize)", "disease": "No disease found, Healthy"},
    11: {"plant": "Grape", "disease": "Black rot"},
    12: {"plant": "Grape", "disease": "Esca (Black Measles)"},
    13: {"plant": "Grape", "disease": "Leaf blight (Isariopsis Leaf Spot)"},
    14: {"plant": "Grape", "disease": "No disease found, Healthy"},
    15: {"plant": "Orange", "disease": "Haunglongbing (Citrus greening)"},
    16: {"plant": "Peach", "disease": "Bacterial spot"},
    17: {"plant": "Peach", "disease": "No disease found, Healthy"},
    18: {"plant": "Pepper,_bell", "disease": "Bacterial_spot"},
    19: {"plant": "Pepper,_bell", "disease": "No disease found, Healthy"},
    20: {"plant": "Potato", "disease": "Early blight"},
    21: {"plant": "Potato", "disease": "Late blight"},
    22: {"plant": "Potato", "disease": "No disease found, Healthy"},
    23: {"plant": "Raspberry", "disease": "No disease found, Healthy"},
    24: {"plant": "Soybean", "disease": "No disease found, Healthy"},
    25: {"plant": "Squash", "disease": "Powdery mildew"},
    26: {"plant": "Strawberry", "disease": "Leaf scorch"},
    27: {"plant": "Strawberry", "disease": "No disease found, Healthy"},
    28: {"plant": "Tomato", "disease": "Bacterial spot"},
    29: {"plant": "Tomato", "disease": "Early blight"},
    30: {"plant": "Tomato", "disease": "Late blight"},
    31: {"plant": "Tomato", "disease": "Leaf Mold"},
    32: {"plant": "Tomato", "disease": "Septoria leaf spot"},
    33: {"plant": "Tomato", "disease": "Spider mites Two-spotted spider mite"},
    34: {"plant": "Tomato", "disease": "Target Spot"},
    35: {"plant": "Tomato", "disease": "Tomato Yellow Leaf Curl Virus"},
    36: {"plant": "Tomato", "disease": "Tomato mosaic virus"},
    37: {"plant": "Tomato", "disease": "No disease found, Healthy"}
}



# Preprocessing function
# Function to Load and Preprocess the Image using Pillow
def load_and_preprocess_image(image_path, target_size=(224, 224)):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0  # normalize
    img_array = np.expand_dims(img_array, axis=0)  # shape: (1, 224, 224, 3)
    return img_array

# Function to Predict the Class of an Image
def predict_image_class(model, image_path, class_indices):
    preprocessed_img = load_and_preprocess_image(image_path)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[predicted_class_index]
    return predicted_class_name

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    #img_array = preprocess_image(file.read())
    predicted_class_name = predict_image_class(model, file, class_indices)
    #confidence = float(np.max(prediction))

    return jsonify({'class': predicted_class_name})
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
