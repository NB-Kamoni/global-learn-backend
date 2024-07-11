#!/usr/bin/env python3
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, render_template
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from flask_restful import Api, Resource
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

# Route to add a student
@app.route("/students", methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(
        name=data['name'],
        date_of_birth=data['date_of_birth'],
        email=data['email'],
        reg_no=data['reg_no'],
        enrollment_date=date.today()  # Set enrollment_date to current date
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully'}), 201

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

@app.route("/")
def index():
    return render_template('index.html')


#Add the routes and views here
#Courses
class Courses(Resource):
    def get(self):
        courses_dict_list = [course.to_dict() for course in Course.query.all()]
        response = make_response(courses_dict_list,200)
        return response
    
    def post(self):
        new_course = Course(
            name = request.form['name'],
            description = request.form['description'],
            teacher_id = request.form['teacher_id'],
            course_code = request.form['course_code'],
            duration_years = request.form['duration_years']
        )
        db.session.add(new_course)
        db.session.commit()

        res_dict = new_course.to_dict()
        response = make_response(res_dict,201)
        return response
    
api.add_resource(Courses, '/courses')

class CourseById(Resource):
    def get(self, id):
        course = Course.query.filter_by(course_id=id).first().to_dict()
        return make_response(jsonify(course), 200)
    
    def patch(self, id):
        course = Course.query.filter(Course.course_id == id).first()
        for attr in request.form:
            setattr(course,attr,request.form[attr])
        db.session.add(course)
        db.session.commit()

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
    
api.add_resource(CourseById, '/courses/<int:id>')




if __name__ == '__main__':
    app.run(port=5555, debug=True)
