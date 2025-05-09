from pydantic import BaseModel, EmailStr
from typing import List

# Schema for creating a new student
class StudentCreate(BaseModel):
    name: str
    email: EmailStr  # Validates email format


# Schema for creating a new course
class CourseCreate(BaseModel):
    title: str
    description: str


# Schema for enrolling a student in a course
class EnrollmentCreate(BaseModel):
    student_id: int  # References student ID
    course_id: int   # References course ID


# Schema for representing a course without students
class CourseOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True  # Enables ORM compatibility for SQLAlchemy models


# Schema for representing a student, including enrolled courses
class StudentOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    courses: List[CourseOut] = []  # List of enrolled courses

    class Config:
        orm_mode = True  # Allows SQLAlchemy model instances to be serialized


# Minimal student representation for nested responses
class StudentSummary(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # Supports ORM serialization


# Schema for representing a course with enrolled students
class CourseOutWithStudents(BaseModel):
    id: int
    title: str
    description: str
    students: List[StudentSummary] = []  # List of enrolled students

    class Config:
        orm_mode = True  # Ensures proper object serialization
