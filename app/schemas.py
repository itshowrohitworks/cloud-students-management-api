# Defines Request/Response Format:
from pydantic import BaseModel

class StudentCreate(BaseModel):
    name:str
    email:str
    course:str
    semester:int
    cgpa:float

class StudentResponse(StudentCreate):
    id:int

    class Config:
        from_attributes = True