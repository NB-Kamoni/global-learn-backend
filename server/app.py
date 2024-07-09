#!/usr/bin/env python3
from models import db, Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify, render_template
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


@app.route("/")
def index():
    return render_template('index.html')

#Add the routes and views here
class Courses(Resource):
    def get(self):
        courses_dict_list = [course.to_dict() for course in Course.query.all()]
        response = make_response(courses_dict_list,200)
        return response
    
api.add_resource(Courses, '/courses')


if __name__ == '__main__':
    app.run(port=5555, debug=True)