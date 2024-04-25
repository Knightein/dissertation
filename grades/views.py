from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user

from models import required_roles, Grade, Assignment

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
def view_grade(id):
    grade = Grade.query.filter_by(grade_id=id).first_or_404()
    return render_template('grades/view_grade.html', grade=grade)


@grades_blueprint.route('/grade_assignment')
def grade_assignment():
    return render_template('grades/grade_assignment.html')
