from flask import Flask, request,jsonify
import mysql.connector
import re # (regular expression ) used for pattern check
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,create_refresh_token,get_jwt
from datetime import timedelta

##   When a user logs out, their token can be added to this set, and any subsequent requests with that token will be denied.
BLACKLISTED_TOKENS = set()


app = Flask(__name__)

# initialize jwt
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(minutes=7)
app.config['JWT_REFRESH_TOKEN_EXPIRES']=timedelta(days=7)
jwt = JWTManager(app)

# This function is a callback that checks if a token is in the blocklist (blacklist). It is called automatically by Flask-JWT-Extended whenever a protected endpoint is accessed. If the token's unique identifier (jti) is found in the BLACKLISTED_TOKENS set, the function returns True, indicating that the token is invalid and should be denied access.
@jwt.token_in_blocklist_loader
def is_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLISTED_TOKENS


con=mysql.connector.connect(host="localhost",
                             user="root", 
                             password="raza@123",
                               database="restapi_db")


print(con.is_connected())

@app.route('/register',methods=["POST"])
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
    if len(password)!=6:
        return jsonify({"message":"password must be atleast 6 character"})

    
    cursor=con.cursor()

     # duplicate email validation
    email=data["email"]
    query="select * from users where email=%s"
    cursor.execute(query,(email,))
    user=cursor.fetchone()
    if user:
        return jsonify({"message":"email already exitst"}),409


    # Error Handling
    try:
        
        cursor=con.cursor()
        password=data["password"]
        hashed_password=generate_password_hash(password)
        query="insert into users(name,email,password)values(%s,%s,%s)"
        values=(
            data["name"],
            data["email"],
            hashed_password
        )
        cursor.execute(query,values)
        con.commit()
        return jsonify({"message":"user register successfully"}),201
    
    except Exception as e:
        return jsonify({"message":"something went wrong","error":str(e)}),500

    finally:
        cursor.close()
  


@app.route('/login', methods=['POST'])
def login():
    data=request.get_json()

    email=data["email"]
    password=data["password"]

    # email exits check
    cursor=con.cursor()
    cursor.execute("select email from users where email=%s",(email,))
    fetch_Email=cursor.fetchone()
    if fetch_Email is None:
        return jsonify({"message":"worng email"})
    

    # cheack enter password and hash password  same or not
    cursor.execute("select * from users where email=%s",(email,))
    user=cursor.fetchone()
    stored_password=user[3]
    stored_id=user[0]

    if check_password_hash(stored_password,password):

        ## create access token ( generate token ) 
        token=create_access_token(identity=str(stored_id))

        ## create refresh token ( generate refresh token )
        refresh_token=create_refresh_token(identity=str(stored_id))
        return jsonify({"message":"login successfull", "token": token, "refresh_token": refresh_token}),200

    else:
        return jsonify({"message":"wrong password"})

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify({"message": "token refreshed successfully", "token": new_token}), 200
 
@app.route('/add', methods=['POST'])
@jwt_required()
def add_student():

    current_user=get_jwt_identity()

    data=request.get_json()
    print(data)
    cursor=con.cursor()
    query="insert into list(id,name,course)values (%s,%s,%s)"
    value=(
        data["id"],
        data["name"],
        data["course"]

    ) 
    cursor.execute(query,value)
    con.commit()
    return jsonify({"message":"student added successfully","login user":current_user}),201

@app.route('/view',methods=['GET'])
# jwt_required() decorator is used to protect the view_student route. This means that a valid JWT token must be provided in the request headers to access this route. If the token is missing or invalid, the request will be denied.
@jwt_required()
def view_student():

    # get current user identity from token
    current_user = get_jwt_identity()

    cursor=con.cursor()
    cursor.execute("select * from list")
    data=cursor.fetchall()
    return jsonify({"student list": data,"login user": current_user})

@app.route('/update',methods=['PUT'])
@jwt_required()
def update_Student():

     # get current user identity from token
    current_user=get_jwt_identity()

    # json data read
    data=request.get_json()

    # variable extract
    id=data["id"]
    name=data["name"]
    course=data["course"]

    # empty feild check
    if id=="" or name=="" or course=="":
        return jsonify({"message":"all feilds are required"})

    
    # id exis check
    cursor=con.cursor()
    id=data["id"]
    cursor.execute("select id from list where id=%s",(id,))
    result=cursor.fetchone()
    if  result is None:
        return jsonify({"message":"studnet not found","login user":current_user})


    try:
        cursor=con.cursor()
        query="update list set name=%s, course=%s where id=%s"
        value=(
            data["name"],
            data["course"],
            data["id"]
        
        )
        cursor.execute(query,value)
        con.commit()

        # row count check
        if cursor.rowcount==1:
            return jsonify({"message":"student updated"}),200
        else:
            return jsonify({"message":"no record update"}),400


        # eception handling 
    except Exception as e:
        return jsonify({"message":"something went wrong","error":str(e)}),500
        

@app.route('/delete',methods=['DELETE'])
@jwt_required()
def delete_student():

    current_user=get_jwt_identity()

    data=request.get_json()
    id=data["id"]   

    # id exist check
    cursor=con.cursor()
    cursor.execute("select id from list where id=%s",(id,))
    result=cursor.fetchone()
    if result is None:
        return jsonify({"message":"student not found"})


    try:
        cursor=con.cursor()
        query="delete from list where id=%s"
                
        cursor.execute(query,(id,))
        con.commit()

        # row count check
        if cursor.rowcount==1:
            return jsonify({"message":"student deleted","login user":current_user}),200

        else:
            return jsonify({"message":"no record delete"})

    except Exception as e:
        return jsonify({"messsage":"somthing went wrong","error":str(e)}),200


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get the unique identifier of the JWT
    BLACKLISTED_TOKENS.add(jti)  # Add the token's jti to the blacklist
    return jsonify({"message": "Successfully logged out"}), 200

  
   
        

app.run(debug=True)