import os
from dotenv import load_dotenv
from flask import Flask
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

# Define resource endpoints
class StudentResource(Resource):
    def get(self):
        students = Student.query.all()
        return {'students': [student.name for student in students]}

# Add resource endpoints to API
api.add_resource(StudentResource, '/students')

# Main entry point
if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT', 5555), debug=app.config['DEBUG'])
