import os
from dotenv import load_dotenv
from flask import Flask, request
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

# Add resource endpoints to API
api.add_resource(StudentResource, '/students', '/students/<int:student_id>')

# View all students:        GET /students
# Add new student:          POST /students
# Change student data:      PUT /students/<student_id>
# Delete students:          DELETE /students/<student_id>
# Search student by id:     GET /students?student_id=<student_id>
# Search student by reg_no: GET /students?reg_no=<reg_no>
# Search student by email:  GET /students?email=<email>
# Search student by name:   GET /students?name=<name>

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 5555), debug=app.config['DEBUG'])



#___________________________________________________________________________________________________________________________

# -------------------------Teacher RESOURCES--------------------------------------------------

class TeacherResource(Resource):
    def get(self):
        """
        Fetches either all teachers or a specific teacher by teacher_id, email, or name.
        """
        teacher_id = request.args.get('teacher_id')
        email = request.args.get('email')
        name = request.args.get('name')

        if teacher_id:
            teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
            if teacher:
                return {'teacher': teacher.to_dict()}
            else:
                return {'message': 'Teacher not found'}, 404

        elif email:
            teacher = Teacher.query.filter_by(email=email).first()
            if teacher:
                return {'teacher': teacher.to_dict()}
            else:
                return {'message': 'Teacher not found'}, 404

        elif name:
            teachers = Teacher.query.filter(Teacher.name.ilike(f'%{name}%')).all()
            if teachers:
                return {'teachers': [teacher.to_dict() for teacher in teachers]}
            else:
                return {'message': 'Teacher not found'}, 404

        else:
            teachers = Teacher.query.all()
            return {'teachers': [teacher.to_dict() for teacher in teachers]}

    def post(self):
        """
        Registers a new teacher.
        """
        data = request.get_json()
        new_teacher = Teacher(
            name=data.get('name'),
            email=data.get('email'),
            # Add other fields if necessary
        )
        db.session.add(new_teacher)
        db.session.commit()
        return new_teacher.to_dict(), 201

    def put(self, teacher_id):
        """
        Updates information for a specific teacher identified by teacher_id.
        """
        data = request.get_json()
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'message': 'Teacher not found'}, 404

        # Update teacher fields based on data provided
        if 'name' in data:
            teacher.name = data['name']
        if 'email' in data:
            teacher.email = data['email']

        db.session.commit()
        return teacher.to_dict()

    def delete(self, teacher_id):
        """
        Deletes a specific teacher identified by teacher_id.
        """
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'message': 'Teacher not found'}, 404

        db.session.delete(teacher)
        db.session.commit()
        return {'message': 'Teacher deleted'}, 204

# Add resource endpoints to API
api.add_resource(TeacherResource, '/teachers', '/teachers/<int:teacher_id>')

# View all teachers:         GET /teachers
# Add new teacher:           POST /teachers
# Change teacher data:       PUT /teachers/<teacher_id>
# Delete teacher:            DELETE /teachers/<teacher_id>
# Search teacher by id:      GET /teachers?teacher_id=<teacher_id>
# Search teacher by email:   GET /teachers?email=<email>
# Search teacher by name:    GET /teachers?name=<name>

#_______________________________________________________________________________________________________________

# --------------------------Course RESOURCES--------------------------------------------------

class CourseResource(Resource):
    def get(self):
        """
        Fetches either all courses or a specific course by course_id or name.
        """
        course_id = request.args.get('course_id')
        name = request.args.get('name')

        if course_id:
            course = Course.query.filter_by(course_id=course_id).first()
            if course:
                return {'course': course.to_dict()}
            else:
                return {'message': 'Course not found'}, 404

        elif name:
            courses = Course.query.filter(Course.course_name.ilike(f'%{name}%')).all()
            if courses:
                return {'courses': [course.to_dict() for course in courses]}
            else:
                return {'message': 'Course not found'}, 404

        else:
            courses = Course.query.all()
            return {'courses': [course.to_dict() for course in courses]}

    def post(self):
        """
        Registers a new course.
        """
        data = request.get_json()
        new_course = Course(
            course_name=data.get('course_name'),
            description=data.get('description'),
            # Add other fields if necessary
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course.to_dict(), 201

    def put(self, course_id):
        """
        Updates information for a specific course identified by course_id.
        """
        data = request.get_json()
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        # Update course fields based on data provided
        if 'course_name' in data:
            course.course_name = data['course_name']
        if 'description' in data:
            course.description = data['description']

        db.session.commit()
        return course.to_dict()

    def delete(self, course_id):
        """
        Deletes a specific course identified by course_id.
        """
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        db.session.delete(course)
        db.session.commit()
        return {'message': 'Course deleted'}, 204

# Add resource endpoints to API
api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>')

# View all courses:          GET /courses
# Add new course:            POST /courses
# Change course data:        PUT /courses/<course_id>
# Delete course:             DELETE /courses/<course_id>
# Search course by id:       GET /courses?course_id=<course_id>
# Search course by name:     GET /courses?name=<name>




#___________________________________________________________________________________________________________


# --------------------------Student Profiles RESOURCES--------------------------------------------------

class StudentProfileResource(Resource):
    def get(self, student_id):
        """
        Fetches the profile of a specific student identified by student_id.
        The profile includes bio, photo_url, name, and reg_no of the student.
        """
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        if student_profile:
            return {
                'student_id': student_id,
                'name': student_profile.student.name,
                'reg_no': student_profile.student.reg_no,
                'bio': student_profile.bio,
                'photo_url': student_profile.photo_url
            }
        else:
            return {'message': 'Student profile not found'}, 404

    def post(self, student_id):
        """
        Creates a new profile for the student identified by student_id.
        """
        data = request.get_json()
        new_profile = StudentProfile(
            bio=data.get('bio'),
            photo_url=data.get('photo_url'),
            student_id=student_id
        )
        db.session.add(new_profile)
        db.session.commit()
        return new_profile.to_dict(), 201

    def put(self, student_id):
        """
        Updates the profile of the student identified by student_id.
        """
        data = request.get_json()
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        if not student_profile:
            return {'message': 'Student profile not found'}, 404

        # Update profile fields based on data provided
        if 'bio' in data:
            student_profile.bio = data['bio']
        if 'photo_url' in data:
            student_profile.photo_url = data['photo_url']

        db.session.commit()
        return student_profile.to_dict()

    def delete(self, student_id):
        """
        Deletes the profile of the student identified by student_id.
        """
        student_profile = StudentProfile.query.filter_by(student_id=student_id).first()
        if not student_profile:
            return {'message': 'Student profile not found'}, 404

        db.session.delete(student_profile)
        db.session.commit()
        return {'message': 'Student profile deleted'}, 204

# Add resource endpoints to API
api.add_resource(StudentProfileResource, '/student-profiles/<int:student_id>')

# Fetch student profile:      GET /student-profiles/<student_id>
# Returns the profile information (bio, photo_url) along with the student's name and reg_no.

# Create new student profile: POST /student-profiles/<student_id>
# Creates a new profile for the student identified by student_id.
    
# Update student profile:     PUT /student-profiles/<student_id>
# Updates the profile of the student identified by student_id.

# Delete student profile:     DELETE /student-profiles/<student_id>
# Deletes the profile of the student identified by student_id.



#___________________________________________________________________________________

# --------------------------Teacher Profiles RESOURCES--------------------------------------------------
# Display All

class TeacherProfileResource(Resource):
    def get(self, teacher_id):
        """
        Fetches the profile of a specific teacher identified by teacher_id.
        The profile includes bio, photo_url, name, email, and other details.
        """
        teacher_profile = TeacherProfile.query.filter_by(teacher_id=teacher_id).first()
        if teacher_profile:
            return {
                'teacher_id': teacher_id,
                'name': teacher_profile.teacher.name,
                'email': teacher_profile.teacher.email,
                'bio': teacher_profile.bio,
                'photo_url': teacher_profile.photo_url,
                'phone_no': teacher_profile.phone_no
            }
        else:
            return {'message': 'Teacher profile not found'}, 404

    def post(self, teacher_id):
        """
        Creates a new profile for the teacher identified by teacher_id.
        """
        data = request.get_json()
        new_profile = TeacherProfile(
            bio=data.get('bio'),
            photo_url=data.get('photo_url'),
            phone_no=data.get('phone_no'),
            teacher_id=teacher_id
        )
        db.session.add(new_profile)
        db.session.commit()
        return new_profile.to_dict(), 201

    def put(self, teacher_id):
        """
        Updates the profile of the teacher identified by teacher_id.
        """
        data = request.get_json()
        teacher_profile = TeacherProfile.query.filter_by(teacher_id=teacher_id).first()
        if not teacher_profile:
            return {'message': 'Teacher profile not found'}, 404

        # Update profile fields based on data provided
        if 'bio' in data:
            teacher_profile.bio = data['bio']
        if 'photo_url' in data:
            teacher_profile.photo_url = data['photo_url']
        if 'phone_no' in data:
            teacher_profile.phone_no = data['phone_no']

        db.session.commit()
        return teacher_profile.to_dict()

    def delete(self, teacher_id):
        """
        Deletes the profile of the teacher identified by teacher_id.
        """
        teacher_profile = TeacherProfile.query.filter_by(teacher_id=teacher_id).first()
        if not teacher_profile:
            return {'message': 'Teacher profile not found'}, 404

        db.session.delete(teacher_profile)
        db.session.commit()
        return {'message': 'Teacher profile deleted'}, 204
    
# Add resource endpoints to API
api.add_resource(TeacherProfileResource, '/teacher-profiles/<int:teacher_id>')

# Fetch teacher profile:      GET /teacher-profiles/<teacher_id>
# Returns the profile information (bio, photo_url, phone_no) along with the teacher's name and email.

# Create new teacher profile: POST /teacher-profiles/<teacher_id>
# Creates a new profile for the teacher identified by teacher_id.
    
# Update teacher profile:     PUT /teacher-profiles/<teacher_id>
# Updates the profile of the teacher identified by teacher_id.

# Delete teacher profile:     DELETE /teacher-profiles/<teacher_id>
# Deletes the profile of the teacher identified by teacher_id.


#_________________________________________________________________________________________________________



# Define Resource for fetching courses enrolled by a specific student
class StudentCoursesResource(Resource):
    def get(self, student_id):
        """
        Fetches all courses enrolled by a specific student identified by student_id.
        """
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        courses = Course.query.join(Enrollment).filter(Enrollment.student_id == student_id).all()
        if not courses:
            return {'message': 'No courses enrolled by this student'}, 404

        return {'courses_enrolled': [course.to_dict() for course in courses]}

# Define Resource for fetching students enrolled in a specific course
class CourseStudentsResource(Resource):
    def get(self, course_id):
        """
        Fetches all students enrolled in a specific course identified by course_id.
        """
        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        students = Student.query.join(Enrollment).filter(Enrollment.course_id == course_id).all()
        if not students:
            return {'message': 'No students enrolled in this course'}, 404

        return {'students_enrolled': [student.to_dict() for student in students]}

# Define Resource for enrolling a student in a course
class EnrollCourseResource(Resource):
    def post(self, student_id, course_id):
        """
        Enrolls a student identified by student_id in a course identified by course_id.
        """
        student = Student.query.get(student_id)
        if not student:
            return {'message': 'Student not found'}, 404

        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if enrollment:
            return {'message': 'Student already enrolled in this course'}, 400

        new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(new_enrollment)
        db.session.commit()
        return {'message': 'Enrolled successfully'}, 201

# Define Resource for deleting a student's enrollment in a course
class DeleteEnrollmentResource(Resource):
    def delete(self, student_id, course_id):
        """
        Deletes the enrollment of a student identified by student_id in a course identified by course_id.
        """
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
        if not enrollment:
            return {'message': 'Enrollment not found'}, 404

        db.session.delete(enrollment)
        db.session.commit()
        return {'message': 'Enrollment deleted successfully'}, 204

# Define Resource for fetching all courses or searching for courses by name
class CourseListResource(Resource):
    def get(self):
        """
        Fetches all courses or searches for courses by name.
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Search courses by name')

        args = parser.parse_args()
        course_name = args.get('name')

        if course_name:
            courses = Course.query.filter(Course.course_name.ilike(f'%{course_name}%')).all()
            if not courses:
                return {'message': 'No courses found with that name'}, 404
            return {'courses': [course.to_dict() for course in courses]}

        courses = Course.query.all()
        return {'courses': [course.to_dict() for course in courses]}

# # Add Resource endpoints to API
api.add_resource(StudentCoursesResource, '/students/<int:student_id>/std_courses')
api.add_resource(CourseStudentsResource, '/courses/<int:course_id>/students')
api.add_resource(EnrollCourseResource, '/students/<int:student_id>/enroll/<int:course_id>')
api.add_resource(DeleteEnrollmentResource, '/students/<int:student_id>/enroll/<int:course_id>')
api.add_resource(CourseListResource, '/courses', '/courses/search')

# Endpoint details:
# - GET /students/<student_id>/courses: Fetches all courses enrolled by a specific student
# - GET /courses/<course_id>/students: Fetches all students enrolled in a specific course
# - POST /students/<student_id>/enroll/<course_id>: Enrolls a student in a course
# - DELETE /students/<student_id>/enroll/<course_id>: Deletes a student's enrollment in a course
# - GET /courses: Fetches all courses
# - GET /courses/search?name=<name>: Searches for courses by name


#_____________________________________________________________________________________________________


# Define Resource for fetching courses taught by a specific teacher
class TeacherCoursesResource(Resource):
    def get(self, teacher_id):
        """
        Fetches all courses taught by a specific teacher identified by teacher_id.
        """
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'message': 'Teacher not found'}, 404

        courses = Course.query.join(TeacherCourse).filter(TeacherCourse.teacher_id == teacher_id).all()
        if not courses:
            return {'message': 'No courses taught by this teacher'}, 404

        return {'courses_taught': [course.to_dict() for course in courses]}

# Define Resource for assigning a course to a teacher
class AssignCourseResource(Resource):
    def post(self, teacher_id, course_id):
        """
        Assigns a course identified by course_id to a teacher identified by teacher_id.
        """
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {'message': 'Teacher not found'}, 404

        course = Course.query.get(course_id)
        if not course:
            return {'message': 'Course not found'}, 404

        teacher_course = TeacherCourse.query.filter_by(teacher_id=teacher_id, course_id=course_id).first()
        if teacher_course:
            return {'message': 'Teacher already assigned to this course'}, 400

        new_teacher_course = TeacherCourse(teacher_id=teacher_id, course_id=course_id)
        db.session.add(new_teacher_course)
        db.session.commit()
        return {'message': 'Course assigned successfully'}, 201

# Define Resource for withdrawing a course from a teacher
class WithdrawCourseResource(Resource):
    def delete(self, teacher_id, course_id):
        """
        Withdraws the course identified by course_id from the teacher identified by teacher_id.
        """
        teacher_course = TeacherCourse.query.filter_by(teacher_id=teacher_id, course_id=course_id).first()
        if not teacher_course:
            return {'message': 'Teacher not assigned to this course'}, 404

        db.session.delete(teacher_course)
        db.session.commit()
        return {'message': 'Course withdrawn successfully'}, 204

# Define Resource for fetching all teachers and their courses
class TeacherListResource(Resource):
    def get(self):
        """
        Fetches all teachers and their assigned courses.
        """
        teachers = Teacher.query.all()
        return {'teachers': [teacher.to_dict() for teacher in teachers]}

# Add Resource endpoints to API
api.add_resource(TeacherCoursesResource, '/teachers/<int:teacher_id>/courses')
api.add_resource(AssignCourseResource, '/teachers/<int:teacher_id>/assign/<int:course_id>')
api.add_resource(WithdrawCourseResource, '/teachers/<int:teacher_id>/withdraw/<int:course_id>')
api.add_resource(TeacherListResource, '/teachers')

# Endpoint details:
# - GET /teachers/<teacher_id>/courses: Fetches all courses taught by a specific teacher
# - POST /teachers/<teacher_id>/assign/<course_id>: Assigns a course to a specific teacher
# - DELETE /teachers/<teacher_id>/withdraw/<course_id>: Withdraws a course from a specific teacher
# - GET /teachers: Fetches all teachers and their assigned courses






# --------------------------Main entry point--------------------------------------------------
if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 5555), debug=app.config['DEBUG'])
