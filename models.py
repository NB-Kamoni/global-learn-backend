from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import date, timedelta
from random import randint, choice
from faker import Faker

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

#--------------------------------------------
class StudentProfile(db.Model, SerializerMixin):
    __tablename__ = 'student_profiles'
    student_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)
    student = db.relationship("Student", back_populates="student_profile", uselist=False)

    serialize_rules = ('-student',)  # Exclude the student relationship during serialization

    def __repr__(self):
        return f'<StudentProfile {self.student_profile_id}>'


class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    reg_no = db.Column(db.String(100), nullable=False)
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profiles.student_profile_id'))

    student_profile = db.relationship('StudentProfile', back_populates='student')
    enrollments = db.relationship('Enrollment', back_populates='student')
    courses = association_proxy('enrollments', 'course')

    serialize_rules = ('-enrollments', '-courses')  # Exclude enrollments and courses relationships during serialization

    def __repr__(self):
        return (f'<Student(student_id={self.student_id}, name={self.name}, '
                f'date_of_birth={self.date_of_birth}, email={self.email}, '
                f'reg_no={self.reg_no}, student_profile_id={self.student_profile_id})>')


class TeacherProfile(db.Model, SerializerMixin):
    __tablename__ = 'teacher_profiles'
    teacher_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    phone_no = db.Column(db.String(20))

    teacher = db.relationship('Teacher', back_populates='teacher_profile', uselist=False)

    serialize_rules = ('-teacher',)  # Exclude the teacher relationship during serialization

    def __repr__(self):
        return f'<TeacherProfile {self.teacher_profile_id}>'


class Teacher(db.Model, SerializerMixin):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    teacher_profile_id = db.Column(db.Integer, db.ForeignKey('teacher_profiles.teacher_profile_id'))

    teacher_profile = db.relationship('TeacherProfile', back_populates='teacher')
    teacher_courses = db.relationship('TeacherCourse', back_populates='teacher')
    courses = association_proxy('teacher_courses', 'course')

    serialize_rules = ('-teacher_courses', '-courses')  # Exclude teacher_courses and courses relationships during serialization

    def __repr__(self):
        return f'<Teacher {self.name}>'


class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    enrollments = db.relationship('Enrollment', back_populates='course')
    teacher_courses = db.relationship('TeacherCourse', back_populates='course')

    serialize_rules = ('-enrollments', '-teacher_courses')  # Exclude enrollments and teacher_courses relationships during serialization

    def __repr__(self):
        return f'<Course {self.course_name}>'


class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))

    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

    serialize_rules = ('-student', '-course')  # Exclude student and course relationships during serialization

    def __repr__(self):
        return f'<Enrollment Student {self.student_id} Course {self.course_id}>'


class TeacherCourse(db.Model, SerializerMixin):
    __tablename__ = 'teacher_courses'
    teacher_course_id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))

    teacher = db.relationship('Teacher', back_populates='teacher_courses')
    course = db.relationship('Course', back_populates='teacher_courses')

    serialize_rules = ('-teacher', '-course')  # Exclude teacher and course relationships during serialization

    def __repr__(self):
        return f'<TeacherCourse Teacher {self.teacher_id} Course {self.course_id}>'
