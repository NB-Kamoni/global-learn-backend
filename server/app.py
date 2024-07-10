from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define API routes
@app.route("/")
def index():
    return render_template('index.html')

# TeacherProfile model
class TeacherProfile(db.Model, SerializerMixin):
    __tablename__ = 'teacher_profiles'
    teacher_profile_id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    phone_no = db.Column(db.Integer)

    teacher = db.relationship('Teacher', back_populates='teacher_profile', uselist=False)

# Teacher model
class Teacher(db.Model, SerializerMixin):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))

    teacher_profile_id = db.Column(db.Integer, db.ForeignKey('teacher_profiles.teacher_profile_id', name='fk_teacher_profiles_teacher_id'))
    teacher_profile = db.relationship('TeacherProfile', back_populates='teacher')

    def __repr__(self):
        return f'<Teacher {self.name}>'

# API routes for Teacher Profiles
@app.route('/teacher_profiles', methods=['GET'])
def get_teacher_profiles():
    teacher_profiles = TeacherProfile.query.all()
    return jsonify([teacher_profile.to_dict() for teacher_profile in teacher_profiles])

@app.route('/teacher_profiles/<int:id>', methods=['GET'])
def get_teacher_profile(id):
    teacher_profile = TeacherProfile.query.get_or_404(id)
    return jsonify(teacher_profile.to_dict())

@app.route('/teacher_profiles', methods=['POST'])
def add_teacher_profile():
    data = request.get_json()
    bio = data.get('bio')
    photo_url = data.get('photo_url')
    phone_no = data.get('phone_no')
    email = data.get('email')

    # Check if email already exists
    existing_teacher = Teacher.query.filter_by(email=email).first()
    if existing_teacher:
        return jsonify(message='Email already exists. Please use a different email.'), 400

    new_teacher_profile = TeacherProfile(bio=bio, photo_url=photo_url, phone_no=phone_no)

    # Create associated Teacher if not already exists
    if not new_teacher_profile.teacher:
        new_teacher = Teacher(email=email)
        new_teacher_profile.teacher = new_teacher

    db.session.add(new_teacher_profile)
    db.session.commit()
    return jsonify(new_teacher_profile.to_dict()), 201

@app.route('/teacher_profiles/<int:id>', methods=['PUT'])
def update_teacher_profile(id):
    teacher_profile = TeacherProfile.query.get_or_404(id)
    data = request.get_json()
    teacher_profile.bio = data.get('bio', teacher_profile.bio)
    teacher_profile.photo_url = data.get('photo_url', teacher_profile.photo_url)
    teacher_profile.phone_no = data.get('phone_no', teacher_profile.phone_no)

    # Handle email update
    new_email = data.get('email')
    if new_email and new_email != teacher_profile.teacher.email:
        existing_teacher = Teacher.query.filter_by(email=new_email).first()
        if existing_teacher:
            return jsonify(message='Email already exists. Please use a different email.'), 400
        teacher_profile.teacher.email = new_email

    db.session.commit()
    return jsonify(teacher_profile.to_dict())

@app.route('/teacher_profiles/<int:id>', methods=['DELETE'])
def delete_teacher_profile(id):
    teacher_profile = TeacherProfile.query.get_or_404(id)
    db.session.delete(teacher_profile)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(port=5555, debug=True)
