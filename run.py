# CSE 106 -- Lab 8
# Python -- run.py

from flask import Flask, render_template,render_template ,url_for, redirect, session, request, flash, jsonify

from flask_jwt_extended import JWTManager

#Flask Login
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Flask Forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired

from database import db, User, Teacher, Student # database model

# Initializes Flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'cse106-lab6-group5'

jwt = JWTManager()

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
                    return url_for('admin') # Use Flask-Admin

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
    return redirect('login.html')

# Student Page



# Teacher Page



# Admin Page



### Main Function ###
if __name__ == '__main__':
    app.app_context()
    with app.app_context():
        db.create_all()
    app.run()
