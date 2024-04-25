from flask import Blueprint, render_template, flash, request
from flask_login import current_user, login_required

from app import db
from assignments.forms import AssignmentForm
from models import Assignment, required_roles

# CONFIG
assignments_blueprint = Blueprint('assignments', __name__, template_folder='templates')


# VIEWS
@assignments_blueprint.route('/assignments', methods=['POST', 'GET'])
@login_required
@required_roles('student')
def assignments():
    # Get all assignments
    all_assignments = Assignment.query.all()

    # If there are assignments
    if len(all_assignments) != 0:
        return render_template('assignments/assignments.html',
                               assignments=all_assignments)
    else:
        flash('No assignments set.')

    return render_template('assignments/assignments.html')


@assignments_blueprint.route('/start_assignment/<id>', methods=['GET', 'POST'])
def start_assignment(id):
    assignment = Assignment.query.filter_by(assignment_id=id).first_or_404()
    return render_template('assignments/start_assignment.html', assignment=assignment)


@assignments_blueprint.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    form = AssignmentForm()

    if form.validate_on_submit():
        new_assignment = Assignment(name=form.assignment_name.data,
                                    description=form.description.data,
                                    due_date=form.due_date.data,
                                    set_by=current_user.firstname + ' ' + current_user.lastname)

        # Add to database
        db.session.add(new_assignment)
        db.session.commit()

        flash('Assignment created successfully!')
        return render_template('assignments/create_assignment.html',
                               form=form,
                               name=current_user.firstname)

    return render_template('assignments/create_assignment.html',
                           form=form,
                           name=current_user.firstname)
