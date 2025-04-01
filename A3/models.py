# models.py
from extensions import db, bcrypt

class Mark(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # New unique identifier
    student_id = db.Column(db.String(80), nullable=False)  
    assignment_name = db.Column(db.String(80), nullable=False)
    mark = db.Column(db.Float, nullable=False)

    # Add any additional fields as needed

class RemarkRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(80), nullable=False)
    assignment_name = db.Column(db.String(80), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    # Add any additional fields as needed

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor = db.Column(db.String(80), nullable=False)
    teaching_feedback = db.Column(db.Text, nullable=False)
    teaching_improvement = db.Column(db.Text, nullable=False)
    labs_feedback = db.Column(db.Text, nullable=False)
    labs_improvement = db.Column(db.Text, nullable=False)
    # Add any additional fields as needed

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'instructor'

    def __init__(self, username, password, user_type):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.user_type = user_type
