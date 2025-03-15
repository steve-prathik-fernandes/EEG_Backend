
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import numpy as np
from tensorflow.keras.models import load_model
from joblib import load
from flask_cors import CORS
import random

from login_signup import login_user, register_user

app=Flask(__name__)
CORS(app)

# Load the model, test data, and label encoder
model = load_model('emotion_detection_model.h5')
X_test_normalized = np.load('X_test_normalized.npy')
le = load('label_encoder.joblib')

@app.route('/analyse', methods=['GET'])
def analyse():
    # Select a random sample from the test data
    n_samples = X_test_normalized.shape[0]  # Number of test samples (e.g., 60)
    random_index = random.randint(0, n_samples - 1)
    sample = X_test_normalized[random_index]  # Shape: (max_length, 310)
    
    # Prepare the sample for prediction (model expects shape: (1, max_length, 310))
    sample = np.expand_dims(sample, axis=0)
    
    # Predict emotion
    prediction = model.predict(sample)  # Output: probabilities for [Anger, Disgust, Fear, Happy]
    predicted_class = np.argmax(prediction, axis=1)[0]  # Get class index (0-3)
    predicted_emotion = le.inverse_transform([predicted_class])[0]  # Map to emotion label
    
    # Return the prediction as JSON
    return jsonify({'emotion': predicted_emotion})

@app.route("/")
def home():
    return "Hello World, from Flask!"

app.config["MONGO_URI"] = "mongodb://localhost:27017/eeg_database"
mongo = PyMongo(app)

@app.route('/get_eeg_data', methods=['GET'])
def get_eeg_data():
    document = mongo.db.eeg_features.find_one({"feature_name": "de_LDS_1"})
    
    if document:
        return jsonify({
            "feature_name": document["feature_name"],
            "data": document["data"]
        })
    else:
        return jsonify({"error": "Data not found"}), 404

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return jsonify(register_user(username, password))

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return jsonify(login_user(username, password))

if __name__=="__main__":
    app.run(debug=True,port=5002)