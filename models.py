# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class StudentProfile(db.Model, SerializerMixin):
    __tablename__ = 'student_profiles'

    student_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(255), nullable=True)

    student = db.relationship("Student", back_populates="profile", uselist=False, overlaps="student_profile")

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
    
    profile = db.relationship("StudentProfile", back_populates="student", uselist=False, overlaps="student_profile")

    def __repr__(self):
        return f'<Student {self.name}>'

class TeacherProfile(db.Model, SerializerMixin):
    __tablename__ = 'teacher_profiles'
    teacher_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    phone_no = db.Column(db.Integer)

    teacher = db.relationship('Teacher', back_populates='teacher_profile', uselist=False)

    def __repr__(self):
        return f'<TeacherProfile {self.teacher_profile_id}>'

class Teacher(db.Model, SerializerMixin):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    teacher_profile_id = db.Column(db.Integer, db.ForeignKey('teacher_profiles.teacher_profile_id'))
    teacher_profile = db.relationship('TeacherProfile', back_populates='teacher')

    courses = db.relationship('Course', back_populates='teacher')

    def __repr__(self):
        return f'<Teacher {self.name}>'

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    course_code = db.Column(db.String(100))

    teacher = db.relationship('Teacher', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course')
    students = association_proxy('enrollments', 'student')

    def __repr__(self):
        return f'<Course {self.name}>'

class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    enrollment_date = db.Column(db.Date)

    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

    def __repr__(self):
        return f'<Enrollment {self.enrollment_id}>'
