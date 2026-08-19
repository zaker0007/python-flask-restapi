from flask import Flask, jsonify, request

app = Flask(__name__)

students=[]
@app.route('/students', methods=['POST'])
def add_student():
    data=request.get_json()
    print(data)
    students.append(data)
    print(students)
    
    return jsonify({"message": "Student added successfully",
                   "students": students}), 200

@app.route('/view', methods=['GET'])
def view():
    return jsonify({"students": students}), 200

@app.route('/update', methods=['PUT'])
def update():
    data=request.get_json()
    for student in students:
        if student['name'] == data['name']:
                student.update(data)
                return jsonify({"message": "Student updated successfully",
                                "students": students}), 200
    return jsonify({"message": "Student not found"}), 404

@app.route('/delete', methods=['DELETE'])
def delete():
    data=request.get_json()
    for student in students:
         if student['name'] == data['name']:
                students.remove(student)
                return jsonify({"message": "Student deleted successfully",
                                "students": students}), 200
    return jsonify({"message": "Student not found"}), 404

app.run(debug=True)