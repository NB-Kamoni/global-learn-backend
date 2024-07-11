#!/usr/bin/env python3
from datetime import datetime

from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask_restful import Api, Resource
from dotenv import load_dotenv
from config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

# Load environment variables from .env file
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
db = SQLAlchemy(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)


# Initialize Flask-RESTful API
api = Api(app)

from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment
##home

@app.route('/')
def index():
    return render_template('index.html')

### Students ###
@app.route('/students', methods=['POST'])
def create_student():
    """
    Create a new student.
    Endpoint: /students
    Method: POST
    """
    data = request.json
    new_student = Student(
        name=data['name'],
        date_of_birth=data['date_of_birth'],
        email=data['email'],
        reg_no=data['reg_no']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student created successfully', 'student_id': new_student.student_id}), 201

@app.route('/students', methods=['GET'])
def get_students():
    """
    Retrieve all students.
    Endpoint: /students
    Method: GET
    """
    students = Student.query.all()
    return jsonify([{'student_id': student.student_id, 'name': student.name, 'email': student.email} for student in students])

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """
    Retrieve a specific student by ID.
    Endpoint: /students/<student_id>
    Method: GET
    """
    student = Student.query.get_or_404(student_id)
    return jsonify({'student_id': student.student_id, 'name': student.name, 'email': student.email})

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    Update a specific student by ID.
    Endpoint: /students/<student_id>
    Method: PUT
    """
    student = Student.query.get_or_404(student_id)
    data = request.json
    student.name = data['name']
    student.date_of_birth = data['date_of_birth']
    student.email = data['email']
    student.reg_no = data['reg_no']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully', 'student_id': student.student_id})

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    Delete a specific student by ID.
    Endpoint: /students/<student_id>
    Method: DELETE
    """
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully', 'student_id': student_id})


### Teachers ###
@app.route('/teachers', methods=['POST'])
def create_teacher():
    """
    Create a new teacher.
    Endpoint: /teachers
    Method: POST
    """
    data = request.json
    new_teacher = Teacher(
        name=data['name'],
        email=data['email']
    )
    db.session.add(new_teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher created successfully', 'teacher_id': new_teacher.teacher_id}), 201

@app.route('/teachers', methods=['GET'])
def get_teachers():
    """
    Retrieve all teachers.
    Endpoint: /teachers
    Method: GET
    """
    teachers = Teacher.query.all()
    return jsonify([{'teacher_id': teacher.teacher_id, 'name': teacher.name, 'email': teacher.email} for teacher in teachers])

@app.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """
    Retrieve a specific teacher by ID.
    Endpoint: /teachers/<teacher_id>
    Method: GET
    """
    teacher = Teacher.query.get_or_404(teacher_id)
    return jsonify({'teacher_id': teacher.teacher_id, 'name': teacher.name, 'email': teacher.email})

@app.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """
    Update a specific teacher by ID.
    Endpoint: /teachers/<teacher_id>
    Method: PUT
    """
    teacher = Teacher.query.get_or_404(teacher_id)
    data = request.json
    teacher.name = data['name']
    teacher.email = data['email']
    db.session.commit()
    return jsonify({'message': 'Teacher updated successfully', 'teacher_id': teacher.teacher_id})

@app.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """
    Delete a specific teacher by ID.
    Endpoint: /teachers/<teacher_id>
    Method: DELETE
    """
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher deleted successfully', 'teacher_id': teacher_id})


### Courses ###
@app.route('/courses', methods=['POST'])
def create_course():
    """
    Create a new course.
    Endpoint: /courses
    Method: POST
    """
    data = request.json
    new_course = Course(
        course_name=data['course_name'],
        description=data['description']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify({'message': 'Course created successfully', 'course_id': new_course.course_id}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    """
    Retrieve all courses.
    Endpoint: /courses
    Method: GET
    """
    courses = Course.query.all()
    return jsonify([{'course_id': course.course_id, 'course_name': course.course_name, 'description': course.description} for course in courses])

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """
    Retrieve a specific course by ID.
    Endpoint: /courses/<course_id>
    Method: GET
    """
    course = Course.query.get_or_404(course_id)
    return jsonify({'course_id': course.course_id, 'course_name': course.course_name, 'description': course.description})

@app.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """
    Update a specific course by ID.
    Endpoint: /courses/<course_id>
    Method: PUT
    """
    course = Course.query.get_or_404(course_id)
    data = request.json
    course.course_name = data['course_name']
    course.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Course updated successfully', 'course_id': course.course_id})

@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """
    Delete a specific course by ID.
    Endpoint: /courses/<course_id>
    Method: DELETE
    """
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully', 'course_id': course_id})


### Enrollments ###
@app.route('/enrollments', methods=['POST'])
def create_enrollment():
    """
    Create a new enrollment.
    Endpoint: /enrollments
    Method: POST
    """
    data = request.json
    new_enrollment = Enrollment(
        student_id=data['student_id'],
        course_id=data['course_id']
    )
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment created successfully', 'enrollment_id': new_enrollment.enrollment_id}), 201

@app.route('/enrollments', methods=['GET'])
def get_enrollments():
    """
    Retrieve all enrollments.
    Endpoint: /enrollments
    Method: GET
    """
    enrollments = Enrollment.query.all()
    return jsonify([{'enrollment_id': enrollment.enrollment_id, 'student_id': enrollment.student_id, 'course_id': enrollment.course_id} for enrollment in enrollments])

@app.route('/enrollments/<int:enrollment_id>', methods=['GET'])
def get_enrollment(enrollment_id):
    """
    Retrieve a specific enrollment by ID.
    Endpoint: /enrollments/<enrollment_id>
    Method: GET
    """
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    return jsonify({'enrollment_id': enrollment.enrollment_id, 'student_id': enrollment.student_id, 'course_id': enrollment.course_id})

@app.route('/enrollments/<int:enrollment_id>', methods=['PUT'])
def update_enrollment(enrollment_id):
    """
    Update a specific enrollment by ID.
    Endpoint: /enrollments/<enrollment_id>
    Method: PUT
    """
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    data = request.json
    enrollment.student_id = data['student_id']
    enrollment.course_id = data['course_id']
    db.session.commit()
    return jsonify({'message': 'Enrollment updated successfully', 'enrollment_id': enrollment.enrollment_id})

@app.route('/enrollments/<int:enrollment_id>', methods=['DELETE'])
def delete_enrollment(enrollment_id):
    """
    Delete a specific enrollment by ID.
    Endpoint: /enrollments/<enrollment_id>
    Method: DELETE
    """
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment deleted successfully', 'enrollment_id': enrollment_id})

@app.route('/teacher-courses', methods=['GET'])
def get_teacher_courses():
    """
    Retrieve all teacher-course assignments.
    Endpoint: /teacher-courses
    Method: GET
    """
    teacher_courses = TeacherCourse.query.all()
    return jsonify([{'teacher_course_id': teacher_course.teacher_course_id, 'teacher_id': teacher_course.teacher_id, 'course_id': teacher_course.course_id} for teacher_course in teacher_courses])

@app.route('/teacher-courses/<int:teacher_course_id>', methods=['GET'])
def get_teacher_course(teacher_course_id):
    """
    Retrieve a specific teacher-course assignment by ID.
    Endpoint: /teacher-courses/<teacher_course_id>
    Method: GET
    """
    teacher_course = TeacherCourse.query.get_or_404(teacher_course_id)
    return jsonify({'teacher_course_id': teacher_course.teacher_course_id, 'teacher_id': teacher_course.teacher_id, 'course_id': teacher_course.course_id})

@app.route('/teacher-courses/<int:teacher_course_id>', methods=['PUT'])
def update_teacher_course(teacher_course_id):
    """
    Update a specific teacher-course assignment by ID.
    Endpoint: /teacher-courses/<teacher_course_id>
    Method: PUT
    """
    teacher_course = TeacherCourse.query.get_or_404(teacher_course_id)
    data = request.json
    teacher_course.teacher_id = data['teacher_id']
    teacher_course.course_id = data['course_id']
    db.session.commit()
    return jsonify({'message': 'Teacher-course assignment updated successfully', 'teacher_course_id': teacher_course.teacher_course_id})

@app.route('/teacher-courses/<int:teacher_course_id>', methods=['DELETE'])
def delete_teacher_course(teacher_course_id):
    """
    Delete a specific teacher-course assignment by ID.
    Endpoint: /teacher-courses/<teacher_course_id>
    Method: DELETE
    """
    teacher_course = TeacherCourse.query.get_or_404(teacher_course_id)
    db.session.delete(teacher_course)
    db.session.commit()
    return jsonify({'message': 'Teacher-course assignment deleted successfully', 'teacher_course_id': teacher_course_id})

@app.route('/teacher-courses', methods=['POST'])
def assign_teacher_course():
    """
    Assign a teacher to a course.
    Endpoint: /teacher-courses
    Method: POST
    """
    data = request.json
    new_teacher_course = TeacherCourse(
        teacher_id=data['teacher_id'],
        course_id=data['course_id']
    )
    db.session.add(new_teacher_course)
    db.session.commit()
    return jsonify({'message': 'Teacher assigned to course successfully', 'teacher_course_id': new_teacher_course.teacher_course_id}), 201



### Student Profiles ###
@app.route('/student-profiles', methods=['POST'])
def create_student_profile():
    """
    Create a new student profile.
    Endpoint: /student-profiles
    Method: POST
    """
    data = request.json
    new_student_profile = StudentProfile(
        bio=data.get('bio'),
        photo_url=data.get('photo_url')
    )
    db.session.add(new_student_profile)
    db.session.commit()
    return jsonify({'message': 'Student profile created successfully', 'student_profile_id': new_student_profile.student_profile_id}), 201

@app.route('/student-profiles', methods=['GET'])
def get_student_profiles():
    """
    Retrieve all student profiles.
    Endpoint: /student-profiles
    Method: GET
    """
    student_profiles = StudentProfile.query.all()
    return jsonify([{'student_profile_id': profile.student_profile_id, 'bio': profile.bio, 'photo_url': profile.photo_url} for profile in student_profiles])

@app.route('/student-profiles/<int:student_profile_id>', methods=['GET'])
def get_student_profile(student_profile_id):
    """
    Retrieve a specific student profile by ID.
    Endpoint: /student-profiles/<student_profile_id>
    Method: GET
    """
    student_profile = StudentProfile.query.get_or_404(student_profile_id)
    return jsonify({'student_profile_id': student_profile.student_profile_id, 'bio': student_profile.bio, 'photo_url': student_profile.photo_url})

@app.route('/student-profiles/<int:student_profile_id>', methods=['PUT'])
def update_student_profile(student_profile_id):
    """
    Update a specific student profile by ID.
    Endpoint: /student-profiles/<student_profile_id>
    Method: PUT
    """
    student_profile = StudentProfile.query.get_or_404(student_profile_id)
    data = request.json
    student_profile.bio = data.get('bio', student_profile.bio)
    student_profile.photo_url = data.get('photo_url', student_profile.photo_url)
    db.session.commit()
    return jsonify({'message': 'Student profile updated successfully', 'student_profile_id': student_profile.student_profile_id})

@app.route('/student-profiles/<int:student_profile_id>', methods=['DELETE'])
def delete_student_profile(student_profile_id):
    """
    Delete a specific student profile by ID.
    Endpoint: /student-profiles/<student_profile_id>
    Method: DELETE
    """
    student_profile = StudentProfile.query.get_or_404(student_profile_id)
    db.session.delete(student_profile)
    db.session.commit()
    return jsonify({'message': 'Student profile deleted successfully', 'student_profile_id': student_profile_id})


### Teacher Profiles ###
@app.route('/teacher-profiles', methods=['POST'])
def create_teacher_profile():
    """
    Create a new teacher profile.
    Endpoint: /teacher-profiles
    Method: POST
    """
    data = request.json
    new_teacher_profile = TeacherProfile(
        bio=data.get('bio'),
        photo_url=data.get('photo_url'),
        phone_no=data.get('phone_no')
    )
    db.session.add(new_teacher_profile)
    db.session.commit()
    return jsonify({'message': 'Teacher profile created successfully', 'teacher_profile_id': new_teacher_profile.teacher_profile_id}), 201

@app.route('/teacher-profiles', methods=['GET'])
def get_teacher_profiles():
    """
    Retrieve all teacher profiles.
    Endpoint: /teacher-profiles
    Method: GET
    """
    teacher_profiles = TeacherProfile.query.all()
    return jsonify([{'teacher_profile_id': profile.teacher_profile_id, 'bio': profile.bio, 'photo_url': profile.photo_url, 'phone_no': profile.phone_no} for profile in teacher_profiles])

@app.route('/teacher-profiles/<int:teacher_profile_id>', methods=['GET'])
def get_teacher_profile(teacher_profile_id):
    """
    Retrieve a specific teacher profile by ID.
    Endpoint: /teacher-profiles/<teacher_profile_id>
    Method: GET
    """
    teacher_profile = TeacherProfile.query.get_or_404(teacher_profile_id)
    return jsonify({'teacher_profile_id': teacher_profile.teacher_profile_id, 'bio': teacher_profile.bio, 'photo_url': teacher_profile.photo_url, 'phone_no': teacher_profile.phone_no})

@app.route('/teacher-profiles/<int:teacher_profile_id>', methods=['PUT'])
def update_teacher_profile(teacher_profile_id):
    """
    Update a specific teacher profile by ID.
    Endpoint: /teacher-profiles/<teacher_profile_id>
    Method: PUT
    """
    teacher_profile = TeacherProfile.query.get_or_404(teacher_profile_id)
    data = request.json
    teacher_profile.bio = data.get('bio', teacher_profile.bio)
    teacher_profile.photo_url = data.get('photo_url', teacher_profile.photo_url)
    teacher_profile.phone_no = data.get('phone_no', teacher_profile.phone_no)
    db.session.commit()
    return jsonify({'message': 'Teacher profile updated successfully', 'teacher_profile_id': teacher_profile.teacher_profile_id})

@app.route('/teacher-profiles/<int:teacher_profile_id>', methods=['DELETE'])
def delete_teacher_profile(teacher_profile_id):
    """
    Delete a specific teacher profile by ID.
    Endpoint: /teacher-profiles/<teacher_profile_id>
    Method: DELETE
    """
    teacher_profile = TeacherProfile.query.get_or_404(teacher_profile_id)
    db.session.delete(teacher_profile)
    db.session.commit()
    return jsonify({'message': 'Teacher profile deleted successfully', 'teacher_profile_id': teacher_profile_id})


if __name__ == '__main__':
    # Use environment variables for Flask configuration
    app.run(port=os.getenv("FLASK_RUN_PORT", 5555), debug=True)