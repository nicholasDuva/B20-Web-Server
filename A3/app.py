# main.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy.exc import IntegrityError
from extensions import db, bcrypt
from student_routes import student_bp
from instructor_routes import instructor_bp
from models import User  # Import User from models.py

app = Flask(__name__, template_folder='src')
app.config['SECRET_KEY'] = 'replace-with-a-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)

# Register Blueprints for student and instructor routes
app.register_blueprint(student_bp)
app.register_blueprint(instructor_bp)

# Create database/tables if they do not already exist
with app.app_context():
    db.create_all()

# Base routes for common pages
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/assignments')
def assignments():
    return render_template('assignments.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/library_resources')
def library_resources():
    return render_template('library_resources.html')

@app.route('/modules')
def modules():
    return render_template('modules.html')

@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Look up the user by username
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Incorrect username or password.", "error")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_type = request.form.get('user_type')

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('register.html')

        new_user = User(username=username, password=password, user_type=user_type)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash("Username already exists. Please choose another.", "error")
            return render_template('register.html')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
