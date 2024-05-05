from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from app import db
from grades.forms import GradeForm
from models import required_roles, Grade, Assignment, User, decrypt

# CONFIG
grades_blueprint = Blueprint('grades', __name__, template_folder='templates')


# VIEWS
@grades_blueprint.route('/grades')
@login_required
@required_roles('student')
def grades():
    # Get all grades for the current user
    all_grades = Grade.query.filter_by(student_id=current_user.id).all()
    all_assignments = Assignment.query.all()

    # If there are grades
    if len(all_grades) != 0:
        return render_template('grades/grades.html',
                               grades=all_grades, assignments=all_assignments)
    else:
        flash('No grades to review.')

    return render_template('grades/grades.html')


@grades_blueprint.route('/view_grade/<id>', methods=['GET', 'POST'])
@login_required
@required_roles('student')
def view_grade(id):
    grade = Grade.query.filter_by(grade_id=id).first_or_404()
    return render_template('grades/view_grade.html', grade=grade)


@grades_blueprint.route('/grade_assignment', methods=['GET', 'POST'])
@login_required
@required_roles('teacher')
def grade_assignment():
    # Get all grades for the current user
    all_grades = Grade.query.all()
    all_assignments = Assignment.query.all()
    all_students = User.query.all()

    # If there are grades
    if len(all_grades) != 0:
        return render_template('grades/grade_assignment.html',
                               grades=all_grades,
                               assignments=all_assignments,
                               students=all_students,
                               name=current_user.firstname)
    else:
        flash('No grades to review.')

    return render_template('grades/grade_assignment.html',
                           name=current_user.firstname)


@grades_blueprint.route('/start_grade/<id>', methods=['GET', 'POST'])
@required_roles('teacher')
def start_grade(id):
    grade = Grade.query.filter_by(grade_id=id).first_or_404()
    # First get the user id from the grade associated with the user
    user_id = grade.student_id
    # Get the postkey
    postkey = User.query.filter_by(id=user_id).first().postkey
    # Decrypt the code
    decrypted_code = decrypt(grade.code_submission, postkey)

    form = GradeForm(grade=grade.grade,
                     feedback=grade.feedback,
                     next_steps=grade.next_steps,
                     correct=grade.correct,
                     code_submission=decrypted_code)

    if form.validate_on_submit():

        # Modify grade
        grade.grade = form.grade.data
        grade.feedback = form.feedback.data
        grade.next_steps = form.next_steps.data
        grade.correct = form.correct.data
        # Add to database
        db.session.commit()

        flash('Grade modified successfully!')
        return render_template('grades/start_grade.html',
                               form=form,
                               grade=grade,
                               code=decrypted_code)

    return render_template('grades/start_grade.html',
                           form=form,
                           grade=grade,
                           code=decrypted_code)
