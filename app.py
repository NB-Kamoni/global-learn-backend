#!/usr/bin/env python3
from datetime import datetime
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
=======
from datetime import date, timedelta, datetime
>>>>>>> e6d9bc9 (updates)
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask_restful import Api, Resource, abort
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)
<<<<<<< HEAD

from models import Student, StudentProfile
=======
def parse_date(date_str):
    """Convert date string in YYYY-MM-DD format to Python date object."""
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}")
# Route to add a student
@app.route("/students", methods=['POST'])
def add_student():
    data = request.get_json()
    print(f"Received data: {data}")
    name = data.get('name')
    date_of_birth = data.get('date_of_birth')
    email = data.get('email')
    reg_no = data.get('reg_no')
    enrollment_date = data.get('enrollment_date')
    completion_date = data.get('completion_date')
    student_profile_id = data.get('student_profile_id')

    # Validate and create student instance
    try:
        new_student = Student(
            name=name,
            date_of_birth=date_of_birth,
            email=email,
            reg_no=reg_no,
            enrollment_date=enrollment_date,
            completion_date=completion_date,
            student_profile_id=student_profile_id
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'message': 'Student added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
# Route to update student information
@app.route("/students/<int:student_id>", methods=['PUT'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    data = request.json
    student.name = data.get('name', student.name)
    student.date_of_birth = data.get('date_of_birth', student.date_of_birth)
    student.email = data.get('email', student.email)
    student.reg_no = data.get('reg_no', student.reg_no)
    db.session.commit()
    return jsonify({'message': 'Student updated successfully'})

# Route to delete a student
@app.route("/students/<int:student_id>", methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

# Route to manage enrollments
@app.route("/enrollments", methods=['POST'])
def enroll_student():
    data = request.json
    student_id = data['student_id']
    course_id = data['course_id']

    enrollment = Enrollment.enroll_student(student_id, course_id)
    if enrollment:
        return jsonify({'message': 'Student enrolled successfully'}), 201
    else:
        return jsonify({'error': 'Failed to enroll student. Course not found.'}), 404

# Route to list all enrollments
@app.route("/enrollments", methods=['GET'])
def list_enrollments():
    enrollments = Enrollment.query.join(Student).join(Course).order_by(
        Enrollment.course_id,
        Enrollment.student_id,
        Enrollment.enrollment_date,
        Enrollment.completion_date
    ).all()

    # Create a list of dictionaries with the detailed data
    enrollment_list = [
        {
            'enrollment_id': enrollment.enrollment_id,
            'enrollment_date': enrollment.enrollment_date.strftime('%Y-%m-%d'),
            'completion_date': enrollment.completion_date.strftime('%Y-%m-%d') if enrollment.completion_date else None,
            'student': {
                'student_id': enrollment.student.student_id,
                'student_name': enrollment.student.name,
                'student_reg_no': enrollment.student.reg_no
            },
            'course': {
                'course_id': enrollment.course.course_id,
                'course_name': enrollment.course.name,
                'duration_years': enrollment.course.duration_years
            }
        }
        for enrollment in enrollments
    ]

    return jsonify(enrollment_list), 200
# Route to view all courses a student is enrolled in
@app.route("/students/<int:student_id>/courses", methods=['GET'])
def get_student_courses(student_id):
    student = Student.query.get_or_404(student_id)
    courses = student.courses
    return jsonify([{
        'course_id': course.course_id,
        'name': course.name,
        'description': course.description
    } for course in courses]), 200

# Route to list all students
@app.route("/students", methods=['GET'])
def list_students():
    students = Student.query.all()
    student_list = [{
        'student_id': student.student_id,
        'name': student.name,
        'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d'),
        'email': student.email,
        'reg_no': student.reg_no,
        'enrollment_date': student.enrollment_date.strftime('%Y-%m-%d') if student.enrollment_date else None,
        'completion_date': student.completion_date.strftime('%Y-%m-%d') if student.completion_date else None
    } for student in students]
    return jsonify(student_list), 200

# Route to list all courses
@app.route("/courses", methods=['GET'])
def list_courses():
    courses = Course.query.all()
    course_list = [{
        'course_id': course.course_id,
        'name': course.name,
        'description': course.description
    } for course in courses]
    return jsonify(course_list), 200
>>>>>>> e6d9bc9 (updates)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    profile = StudentProfile(bio=data.get('bio'), photo_url=data.get('photo_url'))
    db.session.add(profile)
    db.session.flush()  # Ensure the profile ID is available for the student

<<<<<<< HEAD
    # Convert date_of_birth string to a Python date object
    date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()
=======

class Courses(Resource):
    def get(self):
        courses_dict_list = [course.to_dict() for course in Course.query.all()]
        response = make_response(courses_dict_list,200)
        return response
    
    def post(self):
        data = request.json
        new_course = Course(
            name = request.form['name'],
            description = request.form['description'],
            teacher_id = request.form['teacher_id'],
            course_code = request.form['course_code'],
        )
        db.session.add(new_course)
        db.session.commit()
>>>>>>> e6d9bc9 (updates)

    student = Student(
        name=data.get('name'),
        date_of_birth=date_of_birth,
        email=data.get('email'),
        reg_no=data.get('reg_no'),
        student_profile_id=profile.student_profile_id
    )
    db.session.add(student)
    db.session.commit()

    return jsonify(student_id=student.student_id), 201

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        abort(404, description=f"Student with id {id} not found")
    return jsonify({
        'student_id': student.student_id,
        'name': student.name,
        'date_of_birth': student.date_of_birth,
        'email': student.email,
        'reg_no': student.reg_no,
        'profile': {
            'bio': student.profile.bio,
            'photo_url': student.profile.photo_url
        }
    })

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([
        {
            'student_id': student.student_id,
            'name': student.name,
            'date_of_birth': student.date_of_birth,
            'email': student.email,
            'reg_no': student.reg_no,
            'profile': {
                'bio': student.profile.bio,
                'photo_url': student.profile.photo_url
            }
        } for student in students
    ])


<<<<<<< HEAD
=======
        res_dict = course.to_dict()
        response = make_response(res_dict, 200)
        return response
    
    def delete(self, id):
        course = Course.query.filter(Course.course_id == id).first()
        db.session.delete(course)
        db.session.commit()
        res_dict = {"message":"course deleted successfully"}
        response = make_response(res_dict,200)
        return response
    
class EnrollmentResource(Resource):
    def post(self):
        data = request.json
        student_id = data.get('student_id')
        course_id = data.get('course_id')
>>>>>>> e6d9bc9 (updates)

        # Check for missing fields
        if not student_id or not course_id:
            abort(400, message="Missing required fields: student_id and course_id")

        student = Student.query.get(student_id)
        course = Course.query.get(course_id)

        if not student:
            abort(404, message="Student not found")
        if not course:
            abort(404, message="Course not found")

        existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if existing_enrollment:
            abort(400, message="Student already enrolled in this course")

        enrollment_date = date.today()
        completion_date = enrollment_date + timedelta(days=course.duration_years * 365)

        enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
            enrollment_date=enrollment_date,
            completion_date=completion_date
        )

        db.session.add(enrollment)
        db.session.commit()

        return jsonify({'message': 'Student enrolled successfully'}), 201
class EnrollmentUpdateResource(Resource):
    def put(self, enrollment_id):
        enrollment = Enrollment.query.get_or_404(enrollment_id)
        data = request.json

        if 'course_id' in data:
            course = Course.query.get(data['course_id'])
            if course:
                enrollment.course_id = course.course_id
                enrollment.completion_date = enrollment.enrollment_date + timedelta(days=course.duration_years * 365)

        db.session.commit()
        return jsonify({'message': 'Enrollment updated successfully'})

    
api.add_resource(CourseById, '/courses/<int:id>')
api.add_resource(EnrollmentResource, '/enrollments')
api.add_resource(EnrollmentUpdateResource, '/enrollments/<int:enrollment_id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)