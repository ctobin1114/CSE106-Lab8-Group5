# CSE 106 -- Lab 8
# Python -- database.py

from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin


# Defines the access values of the integer user.u_role
ACCESS = {
            'student': 1,
            'teacher': 2,
            'admin': 3
        }

db = SQLAlchemy()


### DB Tables ###

# User table
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    u_id =                  db.Column(db.Integer, primary_key=True)
    u_username =            db.Column(db.String, nullable=False, unique=True)
    u_password =            db.Column(db.String, nullable=False)
    u_role =                db.Column(db.Integer, nullable=False)

    # Returns user id (PK)
    def get_id(self):
        return self.u_id
    
    # Compares given password with a user's password.
    def check_password(self, password):
        return self.u_password == password
    
    # Checks if user is an admin. Returns a bool
    def is_admin(self):
        return self.u_role == ACCESS['admin']
    
    # Checks if user is a teacher. Returns a bool
    def is_teacher(self):
        return self.u_role == ACCESS['teacher']

    # Checks if user is a student. Returns a bool
    def is_student(self):
        return self.u_role == ACCESS['student']
    
    # Compares given access_level to the user's role value. Returns a bool
    def allowed(self, access_level):
        return self.u_role == access_level


# Student table
class Student(db.Model):
    __tablename__ = 'student'

    s_id =                  db.Column(db.Integer, primary_key=True)
    s_user_id =             db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    s_name =                db.Column(db.String, nullable=False)


# Teacher table
class Teacher(db.Model):
    __tablename__ = 'teacher'

    t_id =                  db.Column(db.Integer, primary_key=True)
    t_user_id =             db.Column(db.Integer, db.ForeignKey('user.u_id'), nullable=False)
    t_name =                db.Column(db.String, nullable=False)


# Course table
class Course(db.Model):
    __tablename__ = 'course'

    c_id =                  db.Column(db.Integer, primary_key=True)
    c_teacher_id =          db.Column(db.Integer, db.ForeignKey('teacher.t_id'), nullable=False)
    c_name =                db.Column(db.String, nullable=False)
    c_schedule =            db.Column(db.String, nullable=False)
    c_capacity =            db.Column(db.Integer, nullable=False)


# Grade table
class Grade(db.Model):
    __tablename__ = 'grade'

    g_id =                  db.Column(db.Integer, primary_key=True)
    g_course_id =           db.Column(db.Integer, db.ForeignKey('course.c_id'), nullable=False)
    g_student_id =          db.Column(db.Integer, db.ForeignKey('student.s_id'), nullable=False)
    g_grade =               db.Column(db.Float, nullable=True)

