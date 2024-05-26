from datetime import datetime
from functools import wraps
import os
from models import Properties, User
from bson.objectid import ObjectId 
from flask import Flask, request, jsonify, session
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)

# MongoDB connection string
MONGO_URI = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

client = MongoClient(MONGO_URI)
db = client["rentify_app"]
users_collection = db["users"]
properties_collection = db["properties"]

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app) 


# JWT user lookup loader
@jwt.user_lookup_loader
def load_user(user_id):
    user = users_collection.find_one({"_id": user_id})
    return User(**user) if user else None

# Error handling
@app.errorhandler(HTTPException)
def handle_exception(e):
    response = jsonify({"message": str(e)})
    response.status_code = e.code
    return response

# Registration (POST)
@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        id=str(ObjectId())
        first_name = data.get("first_name")
        email = data.get("email")
        user_type = data.get("user_type")
        password = data.get("password")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")

        required_fields = ["first_name", "email", "user_type", "password"]

        if not all(field in data for field in required_fields):
            return handle_exception(HTTPException(400, "Missing required fields"))

        existing_user = users_collection.find_one({"email": email})
        if not existing_user:

            hashed_password = generate_password_hash(password)
            new_user = User(id, first_name, email, user_type, hashed_password, last_name, phone_number)

            users_collection.insert_one(new_user.__dict__)
            return jsonify({"message": "Registration successful"})
        else:
            return handle_exception(HTTPException(400, "Email already in use"))

    except Exception as e:
       return handle_exception(HTTPException(500, f"Internal Server Error: {str(e)}"))


# Login (POST)
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user_type = data.get("user_type")

        required_fields = ["email", "password", "user_type"]

        if not all(field in data for field in required_fields):
            return handle_exception(HTTPException(400, "Missing required fields"))

        user = users_collection.find_one({"email": email})
        if not user:
            return handle_exception(HTTPException(401, "Invalid credentials"))  # Unauthorized

        if not email or not password or not user_type:
            return handle_exception(HTTPException(400, "Missing email or password"))
        
        if not check_password_hash(user["password"], password):
            return handle_exception(HTTPException(401, "Invalid credentials"))  # Unauthorized

        session["user_id"] = str(user["_id"])
        print(f"User ID: {session['user_id']}")
        access_token = create_access_token(identity=str(user["_id"]))  # Ensure identity is a string
        return jsonify({"message": "Login successful", "access_token": access_token})

    except Exception as e:
        return handle_exception(HTTPException(500, f"Internal Server Error: {str(e)}"))


# Logout (POST)
@app.route("/api/logout", methods=["POST"])
def logout():
    print(f"User ID: {session['user_id']}")
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"})


# login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session["user_id"]:
            return handle_exception(HTTPException(401, "Unauthorized: Not logged in"))
        return f(*args, **kwargs)
    return decorated_function


# Get User Details (GET)
@app.route("/api/user/details", methods=["GET"])
@login_required
def get_user_details():
    try:
        print(f"User ID: {session['user_id']}") 
        user_id = session["user_id"]
        print(f"User ID: {user_id}")
        if not user_id:
            return handle_exception(HTTPException(401, "Unauthorized"))  # Unauthorized

        print(f"User ID: {user_id}")
        user = users_collection.find_one(user_id)
        if not user:
            return handle_exception(HTTPException(404, "User not found"))  # Not Found

        print(f"User: {user}") 
        user.pop("password")
        return jsonify(user)

    except Exception as e:
        return handle_exception(HTTPException(500, f"Internal Server Error: {str(e)}"))


# Create Property (POST)
@app.route('/api/properties', methods=['POST'])
def create_property():
    try:
        property_data = request.get_json()
        # Create a Properties object
        new_property = Properties(
            id=str(ObjectId()),
            seller_id=property_data.get('seller_id'),
            place=property_data.get('place'),
            area=property_data.get('area'),
            price=property_data.get('price'),
            bedrooms=property_data.get('bedrooms'),
            bathrooms=property_data.get('bathrooms'),
            amenities=property_data.get('amenities'),
            description=property_data.get('description'),
            image=property_data.get('image'), 
        )

        # Insert the property into the MongoDB collection
        properties_collection.insert_one(new_property.__dict__)

        return jsonify({'message': 'Property created successfully!'}), 201

    except Exception as e:
        return jsonify({'message': f'Error creating property: {str(e)}'}), 400


# Get Properties all (GET)
@app.route("/api/properties", methods=["GET"])
@jwt_required()
def get_properties():
    try:
        all_properties = properties_collection.find()
        property_list = []
        for property in all_properties:
            # Convert ObjectId to string representation
            property["_id"] = str(property["_id"])
            property_list.append(property)
        return jsonify({"properties": property_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Get Property by id (GET)
@app.route("/api/property/<property_id>", methods=["GET"])
def get_property_details(property_id):
    try:
        property = properties_collection.find_one({"_id": ObjectId(property_id)})
        if property:
            property["_id"] = str(property["_id"])
            return jsonify(property)
        else:
            return handle_exception(HTTPException(404, "Property not found"))
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

# Delete Property by id (DELETE)
@app.route("/api/property/<property_id>", methods=["DELETE"])
def delete_property(property_id):
    try:
        # Check if user has permission to delete the property (optional)
        # ... Implement permission check logic here ...


        property = properties_collection.find_one_and_delete({"_id": ObjectId(property_id)})
        if not property:
            return jsonify({"message": "Property not found"}), 404

        # Perform any additional actions after deletion (optional)
        # ... (e.g., send notifications, update related data) ...

        return jsonify({"message": "Property deleted successfully"})

    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


# Like Property (POST)
@app.route("/api/property/<property_id>/like", methods=["POST"])
@jwt_required()
def like_property(property_id):
    try:
        user_id = get_jwt_identity()
        property = properties_collection.find_one({"_id": ObjectId(property_id)})
        if not property:
            return jsonify({"message": "Property not found"}), 404
        
        properties_collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$inc": {"likes": 1}}
        )
        return jsonify({"message": "Property liked successfully"})
    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


# Interested in Property (POST)
@app.route("/api/property/<property_id>/interested", methods=["POST"])
@jwt_required()
def interested_property(property_id):
    try:
        user_id = get_jwt_identity()
        property = properties_collection.find_one({"_id": ObjectId(property_id)})
        if not property:
            return jsonify({"message": "Property not found"}), 404
        
        properties_collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$addToSet": {"interestedUsers": user_id}}
        )
        # Notify the seller (implement your notification logic here)
        seller_id = property['seller_id']
        # send_notification_to_seller(seller_id, user_id, property_id)
        
        return jsonify({"message": "Interest expressed successfully"})
    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


# Get Users list (GET)
# @app.route("/users", methods=["GET"])
# def get_users():
#     users = users_collection.find()
#     user_list = []
#     for user in users:
#         # Convert ObjectId to string representation
#         user["_id"] = str(user["_id"])
#         user_list.append(user)
#     return jsonify({"users": user_list})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
