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
    