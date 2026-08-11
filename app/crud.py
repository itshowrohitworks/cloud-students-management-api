# Contains Database Queries: Keeps SQL seprate from API.
from sqlalchemy.orm import Session

from app.models import Student
from app.schemas import StudentCreate

from app.models import Student

# POST Request:
def create_student(db:Session,student:StudentCreate):

    db_student = Student(**student.model_dump())

    db.add(db_student)

    db.commit()

    db.refresh(db_student)

    return db_student

# GET Request:
def get_students(db:Session):
    return db.query(Student).all()

def get_student(db:Session,student_id:int):
    return db.query(Student).filter(Student.id == student_id).first()

# PUT Request: (Update)
def update_student(db:Session,student_id:int,student:Student):

    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        return None

    db_student.name = student.name
    db_student.email = student.email
    db_student.course = student.course
    db_student.semester = student.semester
    db_student.cgpa = student.cgpa

    db.commit()

    db.refresh(db_student)

    return db_student

# DELETE Request:
def delete_student(db:Session,student_id:int):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        return None

    db.delete(db_student)
    db.commit()

    return db_student        