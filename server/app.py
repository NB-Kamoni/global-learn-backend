#!/usr/bin/env python3
from datetime import datetime
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
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

from models import Student, StudentProfile

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    profile = StudentProfile(bio=data.get('bio'), photo_url=data.get('photo_url'))
    db.session.add(profile)
    db.session.flush()  # Ensure the profile ID is available for the student

    # Convert date_of_birth string to a Python date object
    date_of_birth = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date()

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





if __name__ == '__main__':
    app.run(port=5555, debug=True)