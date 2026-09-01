import sqlite3
conn=sqlite3.connect('students.db')
c=conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS students (
            fingerprint_id integer PRIMARY KEY,
            roll_no integer not null,
            name text not null
        )""")
def insert_student(stu):
    with conn:
        c.execute("INSERT INTO students values(:fingerprint_id, :roll_no, :name)", {'fingerprint_id':stu.fingerprint_id,'roll_no':stu.roll_no, 'name':stu.name})

def get_stu_by_name(name):
    c.execute("SELECT * FROM students WHERE name=:name",{'name':name})
    return c.fetchall()
def get_students():
    c.execute("SELECT * FROM students")
    return c.fetchall()

def get_stu_by_fingerid(fingerprint_id):
        c.execute("SELECT * FROM students WHERE fingerprint_id=:fingerprint_id",{'fingerprint_id':fingerprint_id})
        return c.fetchall()

def get_stu_by_fingerid(fingerprint_id):
    c.execute("SELECT * FROM students WHERE fingerprint_id=:fingerprint_id",{'fingerprint_id':fingerprint_id})
    return c.fetchone()

def update_name(stu, name):
    with conn:
        c.execute("""UPDATE students SET name=:name WHERE fingerprint_id=:fingerprint_id and roll_no=:roll_no""",
                  {'roll_no': stu.roll_no, 'fingerprint_id': stu.fingerprint_id, 'name': name})
        
def remove_student(stu):
    with conn:
        c.execute("""DELETE from students WHERE fingerprint_id=:fingerprint_id""",
                  {'fingerprint_id':stu.fingerprint_id})
