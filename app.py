from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user  # 0.5.0
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from passlib.hash import sha256_crypt  # 1.7.2
from flask_sqlalchemy import SQLAlchemy  # 2.4.1
from exploring import ex_path
from tasks import td_demo
from datetime import timedelta  # 4.3
from responses import *
import requests_cache
import os


# Defining necessary variables
requests_cache.install_cache('crime_api_cache', backend='sqlite', expire_after=36000)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.config['SECRET_KEY'] = os.urandom(20)
app.register_blueprint(ex_path)
app.register_blueprint(td_demo)

# Initializing Database and Login Service
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
delta = timedelta(hours=2)

# Index page
@app.route('/')
def show_index():
    return render_template('index.html')

# Showing login page
@app.route('/login')
def show_login():
    if current_user.is_authenticated:  # Check if already logged in
        return redirect(url_for('show_explore'))
    return render_template('login.html', response='')

# Performing login
@app.route('/login',  methods=['POST'])
def login_post():
    email = request.form.get('email')  # Getting input from form
    passwd = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()  # Checks user exists
    if not user or not sha256_crypt.verify(passwd, user.passwd):
        flash('Please check your credentials and try again.')
        return redirect(url_for('show_login'))
    # Login user if password matches
    login_user(user, remember=remember, duration=delta)
    return redirect(url_for('show_explore'))

# Loading user from database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Showing signup page
@app.route('/signup')
def show_signup():
    return render_template('signup.html')

# Performing signup
@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')  # Getting input from form
    email = request.form.get('email')
    passwd = request.form.get('password')
    # Check if user exists, try again if yes
    if all([name, email, passwd]):
        check = User.query.filter_by(email=email).first()
        if check:
            flash('Email already exists')
            return redirect(url_for('signup')), 401
        # Add user with hashed password and redirect to login
        user = User(name=name, email=email, passwd=sha256_crypt.encrypt(passwd))
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('show_login')), 201

# Exploring Police API
@app.route('/explore', methods=['GET'])
def show_explore():
    if current_user.is_authenticated:  # Check for valid user
        return render_template('explore.html')
    else:
        return render_template('login.html', response=error_401), 401

# Logging out user
@app.route('/logout')
def logout():
    if current_user.is_authenticated:  # Logout if logged in
        logout_user()
        return render_template('index.html')
    else:  # Login if not logged in
        return render_template('login.html', response=error_401), 401

# Showing Delete user page
@app.route('/delete', methods=['GET'])
def show_delete():
    return render_template('delete.html')

# Performing Delete user
@app.route('/delete', methods=['POST'])
def delete_post():
    name = request.form.get('name')  # Getting input from form
    email = request.form.get('email')
    user = User.query.filter_by(name=name, email=email).first()
    user_tasks = ToDo.query.filter_by(email=email).all()
    print(all([name, email]))
    if all([name, email, user]) and user.email == email:  # Check for valid input
        db.session.delete(user)
        if user_tasks:
            for ut in user_tasks:
                db.session.delete(ut)
        db.session.commit()
        return jsonify(okay_200), 200
    else:
        flash('Invalid information!!!')
        return redirect(url_for('show_delete'))

# Displaying all usrs for admin
@app.route('/all_users', methods=['GET'])
def all_users():  # Check for admin
    if current_user.is_authenticated and current_user.email=='admin@b.com':
        cursor = User.query.all()
        users = [row.serialize() for row in cursor]  # Make sql row json compatible
        return jsonify({'users': users}), 200
    else:
        return render_template('login.html', response=error_401), 401

# Filtering users by name for admin
@app.route('/all_users/<name>', methods=['GET'])
def all_users_name(name):  # Check for admin
    if current_user.is_authenticated and current_user.email=='admin@b.com':
        cursor = User.query.filter_by(name=name).all()
        users = [row.serialize() for row in cursor]  # Make sql row json compatible
        return jsonify({'code': '200',
                        'users': users}), 200
    else:
        return render_template('login.html', response=error_401), 401

# Database Schema for user table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30), unique=True)
    passwd = db.Column(db.String(30))

    # Making sql table row json compatible
    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email}

# Database Schema for to-do table
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), db.ForeignKey('user.email'))
    title = db.Column(db.String(50))
    desc = db.Column(db.String(100))
    status = db.Column(db.String(7))

    # Making sql table row json compatible
    def serialize(self):
        return {"email": self.email,
                "title": self.title,
                "desc": self.desc,
                "status": self.status}

# Running the application
if __name__=="__main__":
    app.run(host='0.0.0.0')
