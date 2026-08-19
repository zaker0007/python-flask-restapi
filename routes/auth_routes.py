## register route
import re# (regular expression ) used for pattern check
import token 

from flask import app, Blueprint, jsonify,request
import models.user_model
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token,create_refresh_token ,get_jwt
from utils.blackkist import BLACKLISTED_TOKENS 
auth_bp=Blueprint("auth",__name__)


@auth_bp.route('/register',methods=["POST"])
def register():
    data=request.get_json()

    # required validation
    if not data.get("name"):
        return jsonify({"messeage":"name is required"})

    # empty validation
    if data["password"]=="":
        return jsonify({"message":"password cannot be empty"})

    # email format validation
    email=data.get("email")
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern,email):
        return jsonify({"message":"invalid email format"}),404

    # password length validation
    password=data.get("password")
    if len(password)<6:
        return jsonify({"message":"password must be atleast 6 character"})


    # response from user_model.py
    success=models.user_model.user_register(data["name"],data["email"],data["password"])
    if not success:
        return jsonify({"message":"email already exitst"}),409

    return jsonify({"message":"user register successfully"}),201

## Login Route
@auth_bp.route('/login',methods=["POST"])

def login():
   

    data=request.get_json() 

    # email validation
    if not data.get("email"):
        return jsonify({"message":"email is required"}),400

    # password validation
    if not data.get("password"):
        return jsonify({"message":"password is required"}),400

    # value extraction
    email=data.get("email")
    password=data.get("password")

    success, token, refresh_token = models.user_model.login_user(data["email"],data["password"])
    if not success:
        return jsonify({"message":"invalid email or password"}),401

    return jsonify({"message":"login successful", "token": token,"refresh_token": refresh_token}),200


# refesh token route

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({"message": "token refreshed successfully", "new token": new_token}), 200


## logout route
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get the unique identifier for the JWT
    BLACKLISTED_TOKENS.add(jti)  # Add the token's jti to the blacklist
    return jsonify({"message": "logout successful"}), 200