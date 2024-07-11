import os
from dotenv import load_dotenv
from flask import Flask
from flask import Flask, request, make_response, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment, TeacherCourse

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

# Create the app context
with app.app_context():
    # Create the database tables if they don't exist
    db.create_all()

# Set up Flask-Restful API
api = Api(app)

# ---------------------Define resource endpoints---------------------------------------------
# -------------------------STUDENT RESOURCES-------------------------------------------------
#Display All


from flask import request
from flask_restful import Resource
from models import db, Student  # Adjust import paths as needed

class StudentResource(Resource):
    def get(self):
        """
        Fetches either all students or a specific student by student_id or reg_no.
        """
        student_id = request.args.get('student_id')
        reg_no = request.args.get('reg_no')

        if student_id:
            student = Student.query.filter_by(student_id=student_id).first()
            if student:
                return {'student': student.to_dict()}
            else:
                return {'message': 'Student not found'}, 404

        elif reg_no:
            student = Student.query.filter_by(reg_no=reg_no).first()
            if student:
                return {'student': student.to_dict()}
            else:
                return {'message': 'Student not found'}, 404

        else:
            students = Student.query.all()
            return {'students': [student.to_dict() for student in students]}

    def post(self):
        """
        Registers a new student.
        """
        data = request.get_json()
        new_student = Student(
            name=data.get('name'),
            date_of_birth=data.get('date_of_birth'),
            email=data.get('email'),
            reg_no=data.get('reg_no')
            # Add other fields if necessary
        )
        db.session.add(new_student)
        db.session.commit()
        return new_student.to_dict(), 201

    def put(self, student_id):
        """
        Updates information for a specific student identified by student_id.
        """
        data = request.get_json()
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        # Update student fields based on data provided
        if 'name' in data:
            student.name = data['name']
        if 'date_of_birth' in data:
            student.date_of_birth = data['date_of_birth']
        if 'email' in data:
            student.email = data['email']
        if 'reg_no' in data:
            student.reg_no = data['reg_no']

        db.session.commit()
        return student.to_dict()

    def delete(self, student_id):
        """
        Deletes a specific student identified by student_id.
        """
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        db.session.delete(student)
        db.session.commit()
        return {'message': 'Student deleted'}, 204

class StudentByRegNoResource(Resource):
    def get(self, reg_no):
        """
        Fetches a specific student by reg_no.
        """
        student = Student.query.filter_by(reg_no=reg_no).first()
        if student:
            return {'student': student.to_dict()}
        else:
            return {'message': 'Student not found'}, 404

#################### Add resource endpoints to API
api.add_resource(StudentResource, '/students', '/students/<int:student_id>')
api.add_resource(StudentByRegNoResource, '/students/by-reg-no/<string:reg_no>')


from flask import request
from flask_restful import Resource
from models import db, Student  # Adjust import paths as needed

class StudentResource(Resource):
    def get(self):
        """
        Fetches either all students or a specific student by student_id, reg_no, email, or name.
        """
        student_id = request.args.get('student_id')
        reg_no = request.args.get('reg_no')
        email = request.args.get('email')
        name = request.args.get('name')

        if student_id:
            student = Student.query.filter_by(student_id=student_id).first()
            if student:
                return {'student': student.to_dict()}
            else:
                return {'message': 'Student not found'}, 404

        elif reg_no:
            student = Student.query.filter_by(reg_no=reg_no).first()
            if student:
                return {'student': student.to_dict()}
            else:
                return {'message': 'Student not found'}, 404

        elif email:
            student = Student.query.filter_by(email=email).first()
            if student:
                return {'student': student.to_dict()}
            else:
                return {'message': 'Student not found'}, 404

        elif name:
            students = Student.query.filter(Student.name.ilike(f'%{name}%')).all()
            if students:
                return {'students': [student.to_dict() for student in students]}
            else:
                return {'message': 'Student not found'}, 404

        else:
            students = Student.query.all()
            return {'students': [student.to_dict() for student in students]}

    def post(self):
        """
        Registers a new student.
        """
        data = request.get_json()
        new_student = Student(
            name=data.get('name'),
            date_of_birth=data.get('date_of_birth'),
            email=data.get('email'),
            reg_no=data.get('reg_no')
            # Add other fields if necessary
        )
        db.session.add(new_student)
        db.session.commit()
        return new_student.to_dict(), 201

    def put(self, student_id):
        """
        Updates information for a specific student identified by student_id.
        """
        data = request.get_json()
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        # Update student fields based on data provided
        if 'name' in data:
            student.name = data['name']
        if 'date_of_birth' in data:
            student.date_of_birth = data['date_of_birth']
        if 'email' in data:
            student.email = data['email']
        if 'reg_no' in data:
            student.reg_no = data['reg_no']

        db.session.commit()
        return student.to_dict()

    def delete(self, student_id):
        """
        Deletes a specific student identified by student_id.
        """
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        db.session.delete(student)
        db.session.commit()
        return {'message': 'Student deleted'}, 204


# View all students:        GET /students
# Add new student:          POST /students
# Change student data:      PUT /students/<student_id>
# Delete students:          DELETE /students/<student_id>
# Search student by id:     GET /students?student_id=<student_id>
# Search student by reg_no: GET /students/by-reg-no/<reg_no>
# Search student by name:   GET /students?name=<name>


# -------------------------Teacher RESOURCES--------------------------------------------------
#Display All
class TeacherResource(Resource):
    def get(self):
        teachers = Teacher.query.all()
        return {'teachers': [teacher.to_dict() for teacher in teachers]}

# Add resource endpoints to API
api.add_resource(TeacherResource, '/teachers')


# --------------------------Course RESOURCES--------------------------------------------------
#Display All

class CourseResource(Resource):
    def get(self):
        courses = Course.query.all()
        return {'courses': [course.to_dict() for course in courses]}

# Add resource endpoints to API
api.add_resource(CourseResource, '/courses')



# --------------------------Teacher Profiles RESOURCES--------------------------------------------------
#Display All

class TeacherProfileResource(Resource):
    def get(self):
        teacher_profiles = TeacherProfile.query.all()
        return {'teacher_profiles': [profile.to_dict() for profile in teacher_profiles]}

# Add resource endpoints to API
api.add_resource(TeacherProfileResource, '/teacher_profiles')


# --------------------------Student Profiles RESOURCES--------------------------------------------------
#Display All
class StudentProfileResource(Resource):
    def get(self):
        student_profiles = StudentProfile.query.all()
        return {'student_profiles': [profile.to_dict() for profile in student_profiles]}

# Add resource endpoints to API
api.add_resource(StudentProfileResource, '/student_profiles')




# --------------------------end--------------------------------------------------
# Main entry point
if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 5555), debug=app.config['DEBUG'])
