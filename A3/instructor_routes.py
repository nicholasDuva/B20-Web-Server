# instructor_routes.py
from flask import Blueprint, render_template, request, session, flash, redirect, url_for, jsonify
from extensions import db
from models import Mark, RemarkRequest, Feedback, User

instructor_bp = Blueprint('instructor', __name__, template_folder='src')

@instructor_bp.route('/instructor/marks')
def view_all_marks():
    if 'user_id' not in session or session.get('user_type') != 'instructor':
        flash("Access denied.", "error")
        return redirect(url_for('login'))
    marks = Mark.query.all()
    return render_template('instructor_marks.html', marks=marks)

@instructor_bp.route('/instructor/feedback')
def view_feedback():
    if 'user_id' not in session or session.get('user_type') != 'instructor':
        flash("Access denied.", "error")
        return redirect(url_for('login'))
    instructor_username = session.get('username')
    feedbacks = Feedback.query.filter_by(instructor=instructor_username).all()
    return render_template('view_feedback.html', feedbacks=feedbacks)

@instructor_bp.route('/instructor/remark_requests')
def view_remark_requests():
    if 'user_id' not in session or session.get('user_type') != 'instructor':
        flash("Access denied.", "error")
        return redirect(url_for('login'))
    requests_list = RemarkRequest.query.all()
    return render_template('view_remark_requests.html', requests=requests_list)

@instructor_bp.route('/instructor/update_remark', methods=['POST'])
def update_remark():
    if 'user_id' not in session or session.get('user_type') != 'instructor':
        return jsonify({"error": "Access denied"}), 403
    remark_id = request.form.get('remark_id')
    new_status = request.form.get('new_status')
    if not remark_id or not new_status:
        return jsonify({"error": "Missing data"}), 400
    remark = RemarkRequest.query.get(remark_id)
    if remark:
        remark.status = new_status
        db.session.commit()
        return jsonify({"message": "Remark request updated successfully!"})
    else:
        return jsonify({"error": "Remark request not found"}), 404

@instructor_bp.route('/instructor/enter_marks', methods=['GET', 'POST'])
def enter_marks():
    if 'user_id' not in session or session.get('user_type') != 'instructor':
        flash("Access denied.", "error")
        return redirect(url_for('login'))
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        assignment_name = request.form.get('assignment_name')
        mark_value = request.form.get('mark')
        if not all([student_id, assignment_name, mark_value]):
            flash("Missing data, please complete the form.", "error")
            return redirect(url_for('instructor.enter_marks'))
        try:
            # Convert mark from string to integer
            mark_value = float(mark_value)
        except ValueError:
            flash("Invalid input. Ensure you have selected a valid student and entered a valid mark.", "error")
            return redirect(url_for('instructor.enter_marks'))
        
        # Check for an existing mark record for the student and assignment
        mark = Mark.query.filter_by(student_id=student_id, assignment_name=assignment_name).first()
        if False:
            mark.mark = mark_value
        else:
            mark = Mark(student_id=student_id, assignment_name=assignment_name, mark=mark_value)
            db.session.add(mark)
        db.session.commit()
        flash("Marks updated successfully!", "success")
        return redirect(url_for('instructor.enter_marks'))
    students = User.query.filter_by(user_type='student').all()
    return render_template('enter_marks.html', students=students)

