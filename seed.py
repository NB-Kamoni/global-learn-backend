from datetime import date
from app import app, db
from models import Student, StudentProfile, Teacher, TeacherProfile, Course, Enrollment

# Create an application context
with app.app_context():
    # Drop all tables and create them again
    db.drop_all()
    db.create_all()

    # Create Student Profiles
    student_profile1 = StudentProfile(bio="Future Fullstack Engineer", photo_url="https://github.com/NB-Kamoni/Images/blob/main/student1.jpg?raw=true")
    student_profile2 = StudentProfile(bio="Aspiring Dev", photo_url="https://github.com/NB-Kamoni/Images/blob/main/student2.jpg?raw=true")

    # Create Teachers
    teacher_profile1 = TeacherProfile(bio="BSc/MSc/PhD", photo_url="https://github.com/NB-Kamoni/Images/blob/main/Teacher1.jpg?raw=true", phone_no=1234567890)
    teacher_profile2 = TeacherProfile(bio="20 Years of Transforming Lives", photo_url="https://github.com/NB-Kamoni/Images/blob/main/Teacher2.jpg?raw=true", phone_no=9876543210)
    
    teacher1 = Teacher(name="Dr. Tena Sana", email="ms@example.com", teacher_profile=teacher_profile1)
    teacher2 = Teacher(name="Prof. Mnoma Pia", email="mp@example.com", teacher_profile=teacher_profile2)

    # Create Courses
    course1 = Course(name="Mathematics", description="Math course", teacher=teacher1, course_code="MATH101", duration_years=4)
    course2 = Course(name="Science", description="Science course", teacher=teacher2, course_code="SCI101", duration_years=5)

    # Add Courses and Teachers to the session and commit to ensure they are created
    db.session.add_all([teacher_profile1, teacher_profile2, teacher1, teacher2, course1, course2])
    db.session.commit()

    # Create Students and Profiles
    student1 = Student(name="Peter Hapa", date_of_birth=date(2000, 1, 1), email="ph@example.com", reg_no="s33/5052/2024", student_profile=student_profile1)
    student2 = Student(name="Mari Dadi", date_of_birth=date(2001, 2, 2), email="kh@example.com", reg_no="s33/4575/2024", student_profile=student_profile2)

    db.session.add_all([student_profile1, student_profile2, student1, student2])
    db.session.commit()

    # Enroll Students
    enrollment1 = Enrollment.enroll_student(student1.student_id, course1.course_id)
    enrollment2 = Enrollment.enroll_student(student2.student_id, course2.course_id)

    if enrollment1 is None:
        print(f"Failed to enroll student1 in course1")
    if enrollment2 is None:
        print(f"Failed to enroll student2 in course2")

    print("Database seeded successfully!")
