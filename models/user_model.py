## this file store  user database related logic


from database import get_connection
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token

def user_register(name,email,password):

    conn=get_connection()
    cursor=conn.cursor()

    try:
        # duplicate email validation
        query="select * from users where email=%s"
        cursor.execute(query,(email,))
        user=cursor.fetchone()
        if user:
            return False

        # password hashing
        hashed_password=generate_password_hash(password)

        #insert user data into database
        query="insert into users(name,email,password) values (%s,%s,%s)"

        cursor.execute(query,(name,email,hashed_password))

        conn.commit()
      

        return  True

    finally:
        cursor.close()
        conn.close()


def login_user(email,password):
    conn=get_connection()
    cursor=conn.cursor()

    try:
        # email exits check
        cursor.execute("select email from users where email=%s",(email,))
        fetch_email=cursor.fetchone()
        if fetch_email is None:
            return False


        # check entered password and hashed password same or not
        cursor.execute("select * from users where email=%s",(email,))
        user=cursor.fetchone()
        stored_id=user[0]
        stored_password=user[3]

        if check_password_hash(stored_password,password):

            # create access token (generate token)
            token=create_access_token(identity=str(stored_id))

            # refresh token (generate refresh token)

            refresh_token=create_refresh_token(identity=str(stored_id))
            return True, token, refresh_token


        else:
            return False

        return True
    finally:
        cursor.close()
        conn.close()


    
