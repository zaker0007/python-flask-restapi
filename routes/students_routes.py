from unittest import result

from flask import Blueprint,  jsonify, request
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required
import models.student_model

student_bp = Blueprint("student", __name__)


## add route

@student_bp.route('/add', methods=['POST'])
@jwt_required()
def add_student():

    data= request.get_json()

    success = models.student_model.add_student(
        data["id"],
          data["name"],
            data["course"]
            ) 
    if not success:
        return jsonify({"message":"student already exists"}),409

    return jsonify({"message":"student added successfully"}),201

# view route

@student_bp.route('/view', methods=['GET'])
@jwt_required()
def view_students():
    current_user = get_jwt_identity()
    students = models.student_model.view_students()
    return jsonify({"students": students, "current_user": current_user}), 200

## update route
@student_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_student():
   current_user = get_jwt_identity()

   data = request.get_json()

   student_id = data.get("id")
   name = data.get("name")
   course = data.get("course")

   # empty feilds check
   if student_id == "" or name == "" or course == "":
       return jsonify({"message": "all fields are required"}), 400



   result = models.student_model.update_student(student_id, name, course)
   if isinstance(result,str):
        return jsonify({"message": result}), 404

   if result ==1:
        return jsonify({"message": "student updated successfully","login user": current_user}), 200

   return jsonify({"message": "no record updated"}), 400


## delete route
@student_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_student():
    current_user=get_jwt_identity()
    data=request.get_json()

    id=data["id"]
    result=models.student_model.delete_student(id)
    if not result:
        return jsonify({"message": "student already deleted"}),404

    return jsonify({"message": "student deleted successfully","login user": current_user}),200
