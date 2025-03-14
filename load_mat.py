from scipy.io import loadmat
import numpy as np
from pymongo import MongoClient

# Load the .mat file
data = loadmat('EEG_features/1.mat')  # Change this to your actual file name

# Extract the 3D data (example: 'de_LDS_1')
if 'de_LDS_1' in data:
    de_lds_1 = data['de_LDS_1']
    print("Shape of de_LDS_1:", de_lds_1.shape)

    # Convert NumPy array to a nested list (MongoDB doesn't support NumPy arrays)
    de_lds_1_list = de_lds_1.tolist()

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["eeg_database"]  # Replace with your database name
    collection = db["eeg_features"]  # Replace with your collection name

    # Insert the data into MongoDB
    document = {
        "feature_name": "de_LDS_1",
        "data": de_lds_1_list
    }
    collection.insert_one(document)
    print("Data inserted into MongoDB!")
else:
    print("Key 'de_LDS_1' not found. Check available keys.")