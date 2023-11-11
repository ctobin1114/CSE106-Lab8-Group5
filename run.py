# CSE 106 -- Lab 8
# Python -- run.py

### Imports ###

from functools import wraps

# Flask Basics
from flask import Flask, render_template,render_template ,url_for, redirect, session, request, flash, jsonify

# Flask Restful
from flask_restful import abort

# Flask JWT
from flask_jwt_extended import JWTManager

# Flask Login
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Flask Admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Flask Forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

# Database & tables
from database import db, ACCESS, User, Student, Teacher, Course, Grade

from sqlalchemy.exc import SQLAlchemyError


### Flask App Config ###

# Initializes Flask app
app = Flask(__name__)

# Configure ???
app.config['SECRET_KEY'] = 'cse106-lab6-group5'
jwt = JWTManager() # Do we need???

# Configure Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Loads user given their ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Initialize database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
db.init_app(app)

# Configure Flask-Admin
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Grade, db.session))



### Login Page ##

# Flask Login Form
class LoginForm (FlaskForm):
    username = StringField( [InputRequired()], render_kw={"placeholder": "Username"} )
    password = PasswordField([InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

# Login page routing
@app.route('/', methods = ['GET', 'POST'])
def login():
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        user = User.query.filter_by(u_username = loginForm.username.data).first()
        
        if user:
            if user.check_password(loginForm.password.data):
                login_user(user)

                if user.is_admin():
                    return redirect('/admin') # Use Flask-Admin

                elif user.is_teacher():
                    teacher = Teacher.query.filter_by(t_user_id=user.u_id).first()
                    if teacher:
                        return redirect(url_for('teacher', t_id=teacher.t_id))

                elif user.is_student():
                    student = Student.query.filter_by(s_user_id=user.u_id).first()
                    if student:
                        return redirect(url_for('student', s_id=student.s_id))
            else:
                flash("Password is incorrect")
             
        else:
            flash("Username does not exist")
    
    return render_template('login.html', form=loginForm)

# Logout
@app.route("/logout", methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('login')



### Student Page ###

# Student Landing Page Routing
@app.route("/student/<int:s_id>")
@login_required
def student(s_id):
    return render_template('student.html', student_id=s_id)

# GET Student's registered courses
@app.route("/student/<int:s_id>/c", methods = ['GET'])
@login_required
def student_courses(s_id):
    records = []

    try:
        
        sql = """
                SELECT  
                    g.g_id, g.g_grade,
                    c.c_name, c.c_schedule,
                    t.t_name, g.g_course_id
                FROM student s, course c, grade g, teacher t
                WHERE s.s_id = ?
                    AND g.g_student_id = s.s_id
                    AND c.c_id = g.g_course_id
                    AND t.t_id = c.c_teacher_id
            """
        
        rows = db.engine.execute(sql, (s_id))
        
        for row in rows:
            record = {}

            record['g_id'] =            row[0]
            record['grade'] =           row[1]
            record['course'] =          row[2]
            record['schedule'] =        row[3]
            record['teacher'] =         row[4]
            record['c_id'] =            row[5]
            
            records.append(record)

        count = len(records)
        response = {'count': count, 'payload': records}
        
        return jsonify(response)
        
    except SQLAlchemyError as e:
        abort(500, error='Could not process request')

# GET available courses and if the student is registered to them
@app.route("/student/<int:s_id>/r", methods = ['GET'])
@login_required
def student_registration_list(s_id):
    records = []

    try:
        
        sql = """
                SELECT
                    c.c_id, c.c_name, c.c_schedule,
                    t.t_name,
                    COUNT(g.g_course_id) AS enrolled, c.c_capacity
                FROM course c, grade g, teacher t
                WHERE c.c_id
                    AND g.g_course_id = c.c_id
                    AND t.t_id = c.c_teacher_id
                GROUP BY c.c_id
            """
        
        rows = db.engine.execute(sql)
        
        sql2 = """
                SELECT
                    g.g_course_id
                FROM grade g
                WHERE g.g_student_id = ?
            """
        
        rows2 = db.engine.execute(sql2, (s_id))

        student_c_ids = []

        for row2 in rows2:
            student_c_ids.append(row2[0])

        for row in rows:
            record = {}

            record['c_id'] =            row[0]
            record['course'] =          row[1]
            record['schedule'] =        row[2]
            record['teacher'] =         row[3]
            record['enrollment'] =      row[4]
            record['capacity'] =        row[5]

            if row[0] in student_c_ids:
                record['student_enrolled'] = True
            else:
                record['student_enrolled'] = False

            records.append(record)

        count = len(records)
        response = {'count': count, 'payload': records}
        
        return jsonify(response)
        
    except SQLAlchemyError as e:
        abort(500, error='Could not process request')

# PUT for registering/dropping a course
# Given a s_id & c_id
# If there is a record in GRADE table where g_student_id = s_id && g_course_id = c_id
# Then delete that record
# Otherwise create a new record in GRADE using s_id & c_id
# Last return an updated registration list
@app.route("/register/<int:s_id>/<int:c_id>", methods = ['PUT'])
@login_required
def student_registration(s_id, c_id):
    try:
        
        sql = """
                SELECT g_id
                FROM grade
                WHERE g_student_id = ?
                    AND g_course_id = ?
            """
        
        rows = db.engine.execute(sql, (s_id, c_id))

        registered = False

        for row in rows:
            if row[0]:
                registered = True
                g_id = row[0]
                break
        
        # If registered, DELETE from grade
        if registered:
            sql =   """
                        DELETE FROM grade
                        WHERE g_id = ?
                    """
            
            db.engine.execute(sql, (g_id))

        # If not registered, POST to grade
        else:
            sql =   """
                        INSERT INTO grade (
                            g_student_id, g_course_id
                        )
                        values(?, ?)
                    """
            
            db.engine.execute(sql, (s_id, c_id))
        
    except SQLAlchemyError as e:
        abort(500, error='Could not process request')

    return jsonify(200)



### Teacher Page ###

# Teacher Landing Page Routing
@app.route("/teacher/<int:t_id>")
@login_required
def teacher(t_id):
    return render_template('teacher.html', teacher_id=t_id)

# GET Teacher Courses
@app.route("/teacher/<int:t_id>/c", methods = ['GET'])
@login_required
def teacher_courses(t_id):
    try:
        records = []

        sql = """
                SELECT
                    c.c_id, c.c_name, c.c_schedule,
                    COUNT(g.g_course_id) AS enrolled, c.c_capacity
                FROM course c, grade g
                WHERE c.c_teacher_id = ?
                    AND g.g_course_id = c.c_id
            """
        
        rows = db.engine.execute(sql, (t_id))

        for row in rows:
            record = {}

            record['c_id'] =            row[0]
            record['course'] =          row[1]
            record['schedule'] =        row[2]
            record['enrollment'] =      row[3]
            record['capacity'] =        row[4]
            
            records.append(record)

        count = len(records)
        response = {'count': count, 'payload': records}
        
        return jsonify(response)

    except SQLAlchemyError as e :
        abort(500, error='Could not process request')

# GET Course Grade
@app.route("/course/<int:c_id>", methods = ['GET'])
@login_required
def teacher_grading(c_id):
    try:
        records = []

        sql = """
                SELECT
                    g.g_id,
                    s.s_name,
                    g.g_grade
                FROM course c, student s, grade g
                WHERE c.c_id = ?
                    AND g.g_course_id = c.c_id
                    AND s.s_id = g.g_student_id
            """
        
        rows = db.engine.execute(sql, (c_id))

        for row in rows:
            record = {}

            record['g_id'] =            row[0]
            record['student'] =         row[1]
            record['grade'] =           row[2]
            
            records.append(record)

        count = len(records)
        response = {'count': count, 'payload': records}
        
        return jsonify(response)

    except SQLAlchemyError as e :
        abort(500, error='Could not process request')

# PUT Student Grade
@app.route("/grade/<int:g_id>/<float:grade>", methods = ['PUT'])
@login_required
def update_grade(g_id, grade):
    try:
        sql =   """ 
                    UPDATE grade
                    SET g_grade = ?
                    WHERE g_id = ?
                """
        
        input = (grade, g_id)

        db.engine.execute(sql, input)
        
    except SQLAlchemyError as e :
        abort(500, error='Could not process request')
    
    return jsonify(200)



### Error Handling ###

# 404 not found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e)), 404



### Main Function ###
if __name__ == '__main__':
    app.app_context()
    # with app.app_context():
    #     db.create_all()
    app.run()
