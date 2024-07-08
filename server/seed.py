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

    # Create Students
    student1 = Student(name="Peter Hapa", date_of_birth=date(2000, 1, 1), email="ph@example.com", reg_no="s33/5052/2024", student_profile=student_profile1)
    student2 = Student(name="Mari Dadi", date_of_birth=date(2001, 2, 2), email="kh@example.com", reg_no="s33/4575/2024", student_profile=student_profile2)

    # Create Teacher Profiles
    teacher_profile1 = TeacherProfile(bio="BSc/MSc/PhD", photo_url="https://github.com/NB-Kamoni/Images/blob/main/Teacher1.jpg?raw=true", phone_no=1234567890)
    teacher_profile2 = TeacherProfile(bio="20 Years of Transforming Lives", photo_url="https://github.com/NB-Kamoni/Images/blob/main/Teacher2.jpg?raw=true", phone_no=9876543210)

    # Create Teachers
    teacher1 = Teacher(name="Dr. Tena Sana", email="ms@example.com", teacher_profile=teacher_profile1)
    teacher2 = Teacher(name="Prof. Mnoma Pia", email="mp@example.com", teacher_profile=teacher_profile2)

    # Create Courses
    course1 = Course(name="Mathematics", description="Math course", teacher=teacher1, course_code="MATH101")
    course2 = Course(name="Science", description="Science course", teacher=teacher2, course_code="SCI101")

    # Create Enrollments
    enrollment1 = Enrollment(student=student1, course=course1, enrollment_date=date(2023, 1, 1))
    enrollment2 = Enrollment(student=student2, course=course2, enrollment_date=date(2023, 2, 1))

    # Add to session and commit
    db.session.add_all([student_profile1, student_profile2, student1, student2, teacher_profile1, teacher_profile2, teacher1, teacher2, course1, course2, enrollment1, enrollment2])
    db.session.commit()

    print("Database seeded successfully!")
