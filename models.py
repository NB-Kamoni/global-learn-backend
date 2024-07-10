# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import date, timedelta

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class StudentProfile(db.Model, SerializerMixin):
    __tablename__ = 'student_profiles'
    student_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))

    student = db.relationship('Student', back_populates='student_profile', uselist=False)

    # add serialization rules
    serialize_rules = ('-student.studentProfile',)

    def __repr__(self):
        return f'<StudentProfile {self.student_profile_id}>'

class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(100))
    reg_no = db.Column(db.String(120))
    enrollment_date = db.Column(db.Date, nullable=True)
    completion_date = db.Column(db.Date, nullable=True)
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profiles.student_profile_id'))
    
    student_profile = db.relationship('StudentProfile', back_populates='student')
    enrollments = db.relationship('Enrollment', back_populates='student')
    courses = association_proxy('enrollments', 'course')

    # add serialization rules
    serialize_rules = ('-student_profile.student','-enrollments.student')


    def __repr__(self):
        return f'<Student {self.name}>'

class TeacherProfile(db.Model, SerializerMixin):
    __tablename__ = 'teacher_profiles'
    teacher_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    phone_no = db.Column(db.Integer)

    teacher = db.relationship('Teacher', back_populates='teacher_profile', uselist=False)

    # add serialization rules
    serialize_rules = ('-teacher.teacherProfile',)


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

    # add serialization rules
    serialize_rules = ('-teacher_profile.teacher','-courses.teacher')


    def __repr__(self):
        return f'<Teacher {self.name}>'

class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))
    course_code = db.Column(db.String(100))
    duration_years = db.Column(db.Integer, nullable=False)  # Duration in years

    teacher = db.relationship('Teacher', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course')
    students = association_proxy('enrollments', 'student')

    # add serialization rules
    serialize_rules = ('-teacher.course','-enrollments.course')

    def __repr__(self):
        return f'<Course {self.name}>'

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'))
    enrollment_date = db.Column(db.Date, default=date.today())
    completion_date = db.Column(db.Date, nullable=True)
    duration_years = db.Column(db.Integer, nullable=True)  # Assuming duration in years

    student = db.relationship('Student', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')

    # add serialization rules
    serialize_rules = ('-student.enrollments','-course.enrollments')


    def __repr__(self):
        return f'<Enrollment {self.enrollment_id}>'

    @classmethod
    def enroll_student(cls, student_id, course_id):
        course = Course.query.get(course_id)
        student = Student.query.get(student_id)

        if not course:
            print(f"Course with ID {course_id} not found.")
            return None

        if not student:
            print(f"Student with ID {student_id} not found.")
            return None

        enrollment_date = date.today()
        completion_date = enrollment_date + timedelta(days=course.duration_years * 365)  # Calculate completion date

        # Create a new enrollment
        new_enrollment = cls(
            student_id=student_id,
            course_id=course_id,
            enrollment_date=enrollment_date,
            completion_date=completion_date,
            duration_years=course.duration_years
        )

        # Update student's enrollment details
        student.enrollment_date = enrollment_date
        student.completion_date = completion_date

        db.session.add(new_enrollment)
        db.session.commit()

        return new_enrollment
