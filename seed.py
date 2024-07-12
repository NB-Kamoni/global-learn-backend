import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment, TeacherCourse
from faker import Faker
from datetime import date, timedelta
from random import randint, choice

# Load environment variables
load_dotenv()

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
db.init_app(app)

# Seed function to populate the database
def seed_data():
    fake = Faker()

    # Seed student profiles
    student_profiles = []
    for _ in range(10):
        student_profile = StudentProfile(
            bio=fake.paragraph(),
            photo_url=fake.image_url()
        )
        db.session.add(student_profile)
        student_profiles.append(student_profile)
    
    db.session.commit()

    # Seed students
    students = []
    for _ in range(20):
        student = Student(
            name=fake.name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=25),
            email=fake.email(),
            reg_no=fake.uuid4(),
            student_profile_id=choice(student_profiles).student_profile_id
        )
        db.session.add(student)
        students.append(student)
    
    db.session.commit()

    # Seed teacher profiles
    teacher_profiles = []
    for _ in range(5):
        teacher_profile = TeacherProfile(
            bio=fake.paragraph(),
            photo_url=fake.image_url(),
            phone_no=fake.phone_number()[:10]
        )
        db.session.add(teacher_profile)
        teacher_profiles.append(teacher_profile)
    
    db.session.commit()

    # Seed teachers
    teachers = []
    for _ in range(8):
        teacher = Teacher(
            name=fake.name(),
            email=fake.email(),
            teacher_profile_id=choice(teacher_profiles).teacher_profile_id
        )
        db.session.add(teacher)
        teachers.append(teacher)
    
    db.session.commit()

    # Seed courses
    courses = []
    course_names = ["Mathematics", "Physics", "History", "Biology", "Chemistry", "Literature", "Computer Science", "Geography", "Art", "Music"]
    for name in course_names:
        course = Course(
            course_name=name,
            description=fake.paragraph()
        )
        db.session.add(course)
        courses.append(course)
    
    db.session.commit()

    # Seed enrollments
    for student in students:
        for _ in range(randint(1, 3)):  # Each student enrolls in 1-3 courses
            course = choice(courses)
            enrollment = Enrollment(
                student_id=student.student_id,
                course_id=course.course_id
            )
            db.session.add(enrollment)
    
    db.session.commit()

    # Seed teacher courses
    for teacher in teachers:
        for _ in range(randint(1, 2)):  # Each teacher teaches 1-2 courses
            course = choice(courses)
            teacher_course = TeacherCourse(
                teacher_id=teacher.teacher_id,
                course_id=course.course_id
            )
            db.session.add(teacher_course)
    
    db.session.commit()

    print('Database seeded successfully!')

# Create the app context for database operations
with app.app_context():
    # Drop all tables
    db.drop_all()

    # Create all tables
    db.create_all()

    # Call the seed function
    seed_data()
