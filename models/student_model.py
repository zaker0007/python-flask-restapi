## this file store  student database related logic 

from database import get_connection

## add student function
def add_student(id,name,course):
    con=get_connection()
    cursor=con.cursor()

    try:
        query="insert into list(id,name,course)values (%s,%s,%s)"
        values=(id,name,course)
        cursor.execute(query,values)

        con.commit()
        return True

    finally:
        cursor.close()
        con.close()

## view student function
def view_students():
    con=get_connection()
    cursor=con.cursor()

    try:
        query="select * from list"
        cursor.execute(query)
        students=cursor.fetchall()
        return students

    finally:
        cursor.close()
        con.close()

## update student function
def update_student(student_id, name, course):
    con=get_connection()
    cursor=con.cursor()

    # id exist check
    cursor.execute("select id from list where id=%s", (student_id,))
    existing_student = cursor.fetchone()    
    if existing_student is None:
        return "student id does not exist"

    try:
        query="update list set name=%s, course=%s where id=%s"
        values=(name, course, student_id)
        cursor.execute(query, values)
        con.commit()
        if  cursor.rowcount:
            return True

        else:
            return False

    except Exception as e:
        return str(e)


## delete student function

def delete_student(id):
    con=get_connection()
    cursor=con.cursor()

    # id exists check
    cursor.execute("select id from list where id=%s",(id,))
    result=cursor.fetchone()
    if result is None:
        return "student id does not exits"

    try:
        query="delete from kist where id=%s"
        value=(id,)
        cursor.execute(query,value)
        if cursor.rowcount==1:
            return True

        else:
            return False


    except Exception as e:
        return False