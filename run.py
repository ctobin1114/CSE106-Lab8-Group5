# CSE 106 -- Lab 8
# Python -- run.py

### Imports ###

from functools import wraps

# Flask Basics
from flask import Flask, render_template,render_template ,url_for, redirect, session, request, flash, jsonify

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



### Teacher Page ###

# Teacher Landing Page Routing
@app.route("/teacher/<int:t_id>")
@login_required
def teacher(t_id):
    return render_template('teacher.html', teacher_id=t_id)



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
