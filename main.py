from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, init_db
from models import Student, Course
from schemas import (
    StudentCreate, CourseCreate, EnrollmentCreate,
    StudentOut, CourseOutWithStudents
)

# Initialize FastAPI application
app = FastAPI()

# Set up the database connection and tables
init_db()

@app.get("/")
def root():
    """Root endpoint to provide a welcome message."""
    return {"message": "Welcome to the Student Course Management API"}


@app.post("/students/", response_model=StudentOut)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student, ensuring email uniqueness."""
    if db.query(Student).filter(Student.email == student.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    new_student = Student(name=student.name, email=student.email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)  # Refresh to get updated state
    return new_student


@app.post("/courses/", response_model=CourseOutWithStudents)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course with title and description."""
    new_course = Course(title=course.title, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)  # Ensure updated state is returned
    return new_course


@app.post("/enroll/")
def enroll_student(data: EnrollmentCreate, db: Session = Depends(get_db)):
    """Enroll a student in a course if both exist."""
    student = db.query(Student).filter(Student.id == data.student_id).first()
    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or Course not found")
    
    student.courses.append(course)  # Associate student with the course
    db.commit()
    return {"message": f"Student {student.name} enrolled in {course.title}"}


@app.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Fetch a student by ID."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/courses/{course_id}", response_model=CourseOutWithStudents)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Fetch a course by ID, including enrolled students."""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
