# Entry Point:
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.schemas import StudentCreate,StudentResponse
from app.database import Base,engine,get_db
from app import models,crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Home API:
@app.get("/")
def home():
    return {
        "message":"Cloud Student Management API",
        "status":"Running Successfully!"
    }


# Health API:
"""
A Health Check API is used by cloud platforms to verify that an application is operational before routing client requests.
"""
@app.get("/health")
def health():
    return {
        "status":"healthy"
    }

# Students Data API:
@app.get("/students",response_model=list[StudentResponse])
def get_students(db:Session = Depends(get_db)):
    return crud.get_students(db)

# Dynamic Students Url:
@app.get("/students/{student_id}",response_model=StudentResponse)
def get_students_id(student_id:int,db:Session = Depends(get_db)):
    student = crud.get_student(db,student_id)

    if student is None:
        raise HTTPException(status_code=404,detail="Student not found!")
    return student

"""
AWS Concept
When we deploy to EC2, this changes:

Local:
http://127.0.0.1:8000/students

AWS:
http://<EC2_PUBLIC_IP>:8000/students
Only the address changes—the API code stays exactly the same.
"""

# Post Request: Adding Students
@app.post("/students",response_model=StudentResponse)
def create_students(student:StudentCreate,db:Session = Depends(get_db)):
    return crud.create_student(db,student)

# Put Request: Updating Students:
@app.put("/students/{student_id}",response_model=StudentResponse)
def update_student(
    student:StudentCreate,
    student_id:int,
    db:Session = Depends(get_db),
):
    updated = crud.update_student(db,student_id,student) # type:ignore

    if updated is None:
        raise HTTPException(status_code=404,detail="Student not found!")
    return updated

# Delete Request: Deleting Students:
@app.delete("/students/{student_id}")
def delete_student(student_id:int,db:Session = Depends(get_db)):
    deleted = crud.delete_student(db,student_id)

    if deleted is None:
        raise HTTPException(status_code=404,detail="Student not found!")

    return {"message":f"Student with id {student_id}, deleted successfully!"}


# Database:
@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SHOW TIMEZONE"))
        return {"status":"Database Connected Successfully!"}
    except Exception as e:
        return {"status":f"Connection failed, Error {str(e)}"}