# seed.py
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment, TeacherCourse
from faker import Faker

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

# Create the app context for database operations
with app.app_context():
    # Drop all tables
    db.drop_all()

    # Create all tables
    db.create_all()

    fake = Faker()

    # Seed the database
    for _ in range(10):
        student = Student(
            name=fake.name(),
            date_of_birth=fake.date_of_birth(),
            email=fake.email(),
            reg_no=fake.random_number(digits=8)
        )
        db.session.add(student)

        teacher = Teacher(
            name=fake.name(),
            email=fake.email()
        )
        db.session.add(teacher)

        course = Course(
            course_name=fake.word(),
            description=fake.text()
        )
        db.session.add(course)

    db.session.commit()

    for student in Student.query.all():
        for course in Course.query.all():
            enrollment = Enrollment(
                student_id=student.student_id,
                course_id=course.course_id
            )
            db.session.add(enrollment)

    for teacher in Teacher.query.all():
        for course in Course.query.all():
            teacher_course = TeacherCourse(
                teacher_id=teacher.teacher_id,
                course_id=course.course_id
            )
            db.session.add(teacher_course)

    db.session.commit()

    print('Database seeded successfully!')
