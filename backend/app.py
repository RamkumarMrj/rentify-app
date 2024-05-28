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
# CORS(app)
CORS(app, resources={r"/api/*": {"origins": "*"}},  supports_credentials=True)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

# JWT Manager
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
def load_user(jwt_header, jwt_data):
    user_id = jwt_data["sub"]
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return User(**user) if user else None

# Error handling
@app.errorhandler(HTTPException)
def handle_exception(e):
    if isinstance(e, HTTPException):
        response = jsonify({"message": e.description})
        response.status_code = e.code if e.code else 500
    else:
        response = jsonify({"message": "Internal Server Error"})
        response.status_code = 500
    return response

# Registration (POST)
@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        id=str(ObjectId())
        print(id)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        user_type = data.get("user_type")
        password = data.get("password")
        phone_number = data.get("phone_number")

        required_fields = ["first_name", "email", "user_type", "password"]

        if not all(field in data for field in required_fields):
            return handle_exception(HTTPException(400, "Missing required fields"))

        existing_user = users_collection.find_one({"email": email})
        if existing_user:
            return handle_exception(HTTPException(400, "Email already in use"))

        hashed_password = generate_password_hash(password)
        new_user = User(id, first_name, email, user_type, hashed_password, last_name, phone_number)

        print(new_user)
        print(new_user.__dict__)
        users_collection.insert_one(new_user.__dict__)
        return jsonify({"message": "Registration successful"})

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
        if not user or not check_password_hash(user["password"], password):
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
        if "user_id" not in session:
            return handle_exception(HTTPException(401, "Unauthorized: Not logged in"))
        return f(*args, **kwargs)
    return decorated_function


# Get User Details (GET)
@app.route("/api/user/details", methods=["GET"])
@login_required
def get_user_details():
    try:
        # user_id = session.get("user_id")
        user_id = get_jwt_identity()
        # print(f"User ID: {user_id1}")
        print(f"User ID: {user_id}") 
        if not user_id:
            return handle_exception(HTTPException(401, "Unauthorized"))  # Unauthorized

        # user = users_collection.find_one(user_id)
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return handle_exception(HTTPException(404, "User not found"))  # Not Found

        user["_id"] = str(user["_id"])
        user.pop("password")
        print(f"User: {user}")
        return jsonify(user), 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return handle_exception(HTTPException(500, f"Internal Server Error: {str(e)}"))


# Create Property (POST)
@app.route('/api/properties', methods=['POST'])
@jwt_required()
def create_property():
    try:
        property_data = request.get_json()
        seller_id = get_jwt_identity()
        # Create a Properties object
        # seller_id=property_data.get('seller_id'),
        new_property = Properties(
            id=str(ObjectId()),
            seller_id=seller_id,
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
        return jsonify({'message': 'Property created successfully!', 'property_id': new_property.id}), 201

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
@jwt_required()
def delete_property(property_id):
    try:
        user_id = get_jwt_identity()

        property = properties_collection.find_one_and_delete({"_id": ObjectId(property_id)})
        if not property:
            return jsonify({"message": "Property not found"}), 404

        if property["seller_id"] != user_id:
            return handle_exception(HTTPException(403, "Forbidden: You do not have permission to delete this property"))

        properties_collection.find_one_and_delete({"_id": ObjectId(property_id)})
        return jsonify({"message": "Property deleted successfully"})

    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


# Like Property (POST)
@app.route("/api/property/<property_id>/like", methods=["POST"])
@jwt_required()
def like_property(property_id):
    try:
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
        user = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "first_name": 1, "last_name": 1, "email": 1, "phone_number": 1})
        if not user:
            return handle_exception(HTTPException(404, "User not found"))

        property = properties_collection.find_one({"_id": ObjectId(property_id)})
        if not property:
            return jsonify({"message": "Property not found"}), 404

        interested_user = {
            "user_id": user_id,
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "phone_number": user["phone_number"]
        }

        properties_collection.update_one(
            {"_id": ObjectId(property_id)},
            {"$addToSet": {"interestedUsers": interested_user}}
        )

        return jsonify({"message": "Interest expressed successfully"})
    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


# View Interested Users (GET)
@app.route("/api/property/<property_id>/interested-users", methods=["GET"])
@jwt_required()
def view_interested_users(property_id):
    try:
        user_id = get_jwt_identity()
        property = properties_collection.find_one({"_id": ObjectId(property_id)})
        if not property:
            return jsonify({"message": "Property not found"}), 404

        if property["seller_id"] != user_id:
            return handle_exception(HTTPException(403, "Forbidden: You do not have permission to view this property's interested users"))

        return jsonify({"interestedUsers": property.get("interestedUsers", [])})
    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


# Get Users list (GET)
# @app.route("/users", methods=["GET"])
# def get_users():
    # users = users_collection.find()
    # user_list = []
    # for user in users:
    #     # Convert ObjectId to string representation
    #     user["_id"] = str(user["_id"])
    #     user_list.append(user)
    # return jsonify({"users": user_list})



if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
