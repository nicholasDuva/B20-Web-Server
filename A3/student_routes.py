# student_routes.py
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from extensions import db
from models import Mark, RemarkRequest, Feedback, User

student_bp = Blueprint('student', __name__, template_folder='src')

# Route for students to view their own marks
@student_bp.route('/student_marks')
def student_marks():
    if 'user_id' not in session or session.get('user_type') != 'student':
        flash("Access denied. Only students can view marks.", "error")
        return redirect(url_for('login'))
    student_id = session.get('user_id')
    marks = Mark.query.filter_by(student_id=student_id).all()
    return render_template('student_marks.html', marks=marks)

# AJAX endpoint for submitting a remark request
@student_bp.route('/remark_requests', methods=['POST'])
def remark_requests():
    if 'user_id' not in session or session.get('user_type') != 'student':
        return jsonify({"error": "Access denied. Only students can submit remark requests."}), 403
    student_id = session.get('user_id')
    # print(f"Student id: {student_id}")
    assignment_name = request.form.get('assignment_name')
    reason = request.form.get('reason')
    if not assignment_name or not reason:
        return jsonify({"error": "Missing data"}), 400
    remark = RemarkRequest(student_id=student_id, assignment_name=assignment_name, reason=reason, status='Pending')
    # print(f"{remark}")
    db.session.add(remark)
    db.session.commit()
    return jsonify({"message": "Remark request submitted successfully!"})

# Route for students to submit anonymous feedback
@student_bp.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user_id' not in session or session.get('user_type') != 'student':
        flash("Access denied. Only students can submit feedback.", "error")
        return redirect(url_for('login'))
    if request.method == 'POST':
        instructor_id = request.form.get('instructor')
        teaching_feedback = request.form.get('teaching_feedback')
        teaching_improvement = request.form.get('teaching_improvement')
        labs_feedback = request.form.get('labs_feedback')
        labs_improvement = request.form.get('labs_improvement')
        
        if not all([instructor_id, teaching_feedback, teaching_improvement, labs_feedback, labs_improvement]):
            flash("Please complete all fields.", "error")
            instructors = User.query.filter_by(user_type='instructor').all()
            return render_template('feedback.html', instructors=instructors)
        
        # Query the database to get the instructor's username using the submitted id
        instructor_obj = User.query.get(instructor_id)
        if not instructor_obj:
            flash("Selected instructor does not exist.", "error")
            instructors = User.query.filter_by(user_type='instructor').all()
            return render_template('feedback.html', instructors=instructors)
        
        # Create the feedback object with instructor's username
        fb = Feedback(
            instructor=instructor_obj.username,
            teaching_feedback=teaching_feedback,
            teaching_improvement=teaching_improvement,
            labs_feedback=labs_feedback,
            labs_improvement=labs_improvement
        )
        db.session.add(fb)
        db.session.commit()
        flash("Your feedback has been submitted successfully!", "success")
        return redirect(url_for('student.feedback'))
    
    # For GET, query the instructors and pass to the template
    instructors = User.query.filter_by(user_type='instructor').all()
    return render_template('feedback.html', instructors=instructors)


