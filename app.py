
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

from login_signup import login_user, register_user

app=Flask(__name__)

@app.route("/")
def home():
    return "Hello World, from Flask!"
# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/eeg_database"  # Replace with your database name
mongo = PyMongo(app)

@app.route('/get_eeg_data', methods=['GET'])
def get_eeg_data():
    # Fetch the document containing the 3D data
    document = mongo.db.eeg_features.find_one({"feature_name": "de_LDS_1"})

    if document:
        # Return the 3D data as a JSON response
        return jsonify({
            "feature_name": document["feature_name"],
            "data": document["data"]
        })
    else:
        return jsonify({"error": "Data not found"}), 404
    

# Route to register a new user
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return jsonify(register_user(username, password))

# Route to login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return jsonify(login_user(username, password))
    
if __name__=="__main__":
    app.run(debug=True,port=5002)
