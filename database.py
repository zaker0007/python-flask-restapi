import mysql.connector

def get_connection():
    con=mysql.connector.connect(host="localhost",
                             user="root", 
                             password="raza@123",
                               database="restapi_db")

    return con