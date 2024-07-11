from app import app
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment, TeacherCourse
from faker import Faker
from datetime import date
from random import randint, choice
import os
from datetime import datetime
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask_restful import Api, Resource
from dotenv import load_dotenv
from config import DevelopmentConfig, ProductionConfig, TestingConfig

# Load environment variables from .env file
load_dotenv()
# Create a Flask application context

app.app_context().push()

# Initialize Flask app
app = Flask(__name__)


# Load appropriate configuration based on FLASK_ENV
if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object('config.ProductionConfig')
elif os.getenv('FLASK_ENV') == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

# Configure SQLAlchemy database URI based on environment variables
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set up database URI based on environment (use DB_EXTERNAL_URL by default)
if os.getenv('FLASK_ENV') == 'production':
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_INTERNAL_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_EXTERNAL_URL")

# Set the Flask app secret key from environment variable
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)


# Initialize Flask-RESTful API
api = Api(app)


# Initialize Faker
fake = Faker()

# Function to create random date of birth
def random_date_of_birth(start_year=1990, end_year=2005):
    year = randint(start_year, end_year)
    month = randint(1, 12)
    day = randint(1, 28)  # Simplified to avoid issues with February
    return date(year, month, day)

# Drop all tables and create them again
db.drop_all()
db.create_all()

# Create 10 courses
courses = []
for _ in range(10):
    course = Course(
        course_name=fake.bs(),
        description=fake.text()
    )
    courses.append(course)
    db.session.add(course)

# Create 50 students with profiles
students = []
for _ in range(20):
    # Create a student profile
    student_profile = StudentProfile(
        bio=fake.text(),
        photo_url=fake.image_url()
    )

    # Create a student
    student = Student(
        name=fake.name(),
        date_of_birth=random_date_of_birth(),
        email=fake.email(),
        reg_no=f's{randint(30, 99)}/{randint(1000, 9999)}/{randint(2020, 2025)}',
        student_profile=student_profile
    )
    students.append(student)
    db.session.add(student)

# Create 10 teachers with profiles
teachers = []
for _ in range(20):
    # Create a teacher profile
    teacher_profile = TeacherProfile(
        bio=fake.text(),
        photo_url=fake.image_url(),
        phone_no=fake.phone_number()
    )

    # Create a teacher
    teacher = Teacher(
        name=fake.name(),
        email=fake.email(),
        teacher_profile=teacher_profile
    )
    teachers.append(teacher)
    db.session.add(teacher)

# Commit to save courses, students, and teachers to the database
db.session.commit()

# Enroll students in courses
for student in students:
    for _ in range(randint(1, 5)):  # Each student enrolls in 1 to 5 courses
        enrollment = Enrollment(
            student_id=student.student_id,
            course_id=choice(courses).course_id
        )
        db.session.add(enrollment)

# Assign teachers to courses
for teacher in teachers:
    for _ in range(randint(1, 3)):  # Each teacher teaches 1 to 3 courses
        teacher_course = TeacherCourse(
            teacher_id=teacher.teacher_id,
            course_id=choice(courses).course_id
        )
        db.session.add(teacher_course)

# Commit the session to save the enrollments and teacher course assignments to the database
db.session.commit()

print("Seeding completed successfully!")
