from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# Association table for many-to-many relationship between students and courses
enrollments_table = Table(
    "enrollments", Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),  # Links to Student ID
    Column("course_id", Integer, ForeignKey("courses.id")),    # Links to Course ID
    Column("enrolled_on", DateTime, default=datetime.utcnow)   # Stores enrollment timestamp
)


class Student(Base):
    """Represents a student in the system."""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each student
    name = Column(String)  # Student's name
    email = Column(String, unique=True, index=True)  # Ensures unique email for each student

    # Many-to-many relationship with courses using the enrollment table
    courses = relationship("Course", secondary=enrollments_table, back_populates="students")


class Course(Base):
    """Represents a course available for enrollment."""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each course
    title = Column(String)  # Course title
    description = Column(String)  # Brief description of the course

    # Many-to-many relationship with students using the enrollment table
    students = relationship("Student", secondary=enrollments_table, back_populates="courses")
