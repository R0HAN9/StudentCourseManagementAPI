# Student Course Management API

## A production-ready REST API built with **FastAPI** and **SQLAlchemy** to manage students, courses, and enrollments — supporting both **in-memory SQLite** (for testing) and **PostgreSQL** (for production).

Features

-CRUD operations for Students and Courses
-Many-to-Many relationship with Enrollments
-Email validation using Pydantic’s `EmailStr`
-Pagination on listing endpoints
-Basic unit testing using `pytest`
-Switchable database backend with one flag
-Postman collection for easy API testing

Tech Stack

- Backend: FastAPI, SQLAlchemy
-Validation: Pydantic
-Database: PostgreSQL or SQLite (in-memory)
-Testing: Pytest, FastAPI TestClient
-Documentation: Swagger UI at `/docs`

Setup Instructions

1. Clone the Repo

```bash
git clone https://github.com/R0HAN9/StudentCourseManagementAPI.git
cd StudentCourseManagementAPI


2. Create a Virtual Environment
	python -m venv venv
	source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
	pip install -r requirements.txt

4. Configure Database (Optional)
By default, the app uses in-memory SQLite.

To use PostgreSQL, open database.py and change:
	USE_POSTGRESQL = True

Then update your PostgreSQL credentials:
POSTGRES_URL = "postgresql://postgres:password@localhost:5432/student_db"


Run the Server
uvicorn main:app --reload


API Endpoints

| Method | Endpoint         | Description                    |
| ------ | ---------------- | ------------------------------ |
| GET    | `/`              | Welcome message                |
| POST   | `/students/`     | Create a new student           |
| GET    | `/students/{id}` | Get student + enrolled courses |
| POST   | `/courses/`      | Create a new course            |
| GET    | `/courses/{id}`  | Get course + enrolled students |
| POST   | `/enroll/`       | Enroll student in a course     |
| GET    | `/students/`     | Paginated student list         |
| GET    | `/courses/`      | Paginated course list          |


Sample Request Payloads
	Create a Student

POST /students/
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}


Create a Course
POST /courses/
Content-Type: application/json

{
  "title": "Math 101",
  "description": "Basic mathematics"
}


Enroll Student
POST /enroll/
Content-Type: application/json

{
  "student_id": 1,
  "course_id": 2
}



Postman API Testing

1. Import Postman Collection
A ready-to-use Postman collection is included:
	postman/StudentAPI.postman_collection.json

2. Suggested Test Flow
	POST /students/ → Create a student

	POST /courses/ → Create a course
	POST /enroll/ → Enroll student in course
	GET /students/{id} → Check student details
	GET /courses/{id} → Check course details

You can also test pagination:
	GET /students/?page=1&limit=10
	GET /courses/?page=1&limit=5


Run Unit Tests
pytest


Example Unit Test (test_main.py)

	from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_student():
    response = client.post("/students/", json={
        "name": "Test User",
        "email": "testuser@example.com"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test User"


Notes

Uses orm_mode = True in Pydantic schemas for ORM compatibility
EmailStr ensures valid email input
Pagination uses page and limit query parameters
SQLite resets on restart — use PostgreSQL for persistent data

Author
Rohan Kumar
Open to collaborations, internships, and contributions!
