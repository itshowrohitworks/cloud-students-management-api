# Entry Point:
from fastapi import FastAPI
from app.schemas import StudentCreate

app = FastAPI()

# Dummy Data:
students = [
    {
        "id": 1,
        "name": "Rohit",
        "course": "M.Tech DS & AI"
    },
    {
        "id": 2,
        "name": "Alice",
        "course": "Computer Science"
    }
]

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
@app.get("/students")
def get_students():
    return students

# Dynamic Students Url:
@app.get("/students/{student_id}")
def get_students_id(student_id:int):
    for student in students:
        if student["id"] == student_id:
            return student
    return {
        "message":"Student not found!"
    }

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
@app.post("/students")
def create_students(student:StudentCreate):
    student_data = student.model_dump()
    student_data["id"] = len(students) + 1
    students.append(student_data)
    return {"message":f"Successfully created student, with id {student_data["id"]}"}