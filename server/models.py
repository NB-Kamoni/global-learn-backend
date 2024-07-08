# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

from . import db

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    student_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(100))
    reg_no = db.Column(db.String(100))
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profiles.student_profile_id'))
    student_profile = db.relationship('StudentProfile', back_populates='student')

StudentProfile.student = db.relationship('Student', back_populates='student_profile', uselist=False)

class TeacherProfile(db.Model):
    __tablename__ = 'teacher_profiles'
    teacher_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    phone_no = db.Column(db.Integer)

class Teacher(db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    teacher_profile_id = db.Column(db.Integer, db.ForeignKey('teacher_profiles.teacher_profile_id'))
    teacher_profile = db.relationship('TeacherProfile', back_populates='teacher')

TeacherProfile.teacher = db.relationship('Teacher', back_populates='teacher_profile', uselist=False)

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    course_code = db.Column(db.String(100))

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    enrollment_date = db.Column(db.Date)
