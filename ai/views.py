from flask import Blueprint, request, render_template, flash
from ai import llm
from app import db
from models import Assignment, Grade

ai_blueprint = Blueprint('ai', __name__, template_folder='templates')


# VIEWS
@ai_blueprint.route('/submit_assignment', methods=['GET', 'POST'])
def submit_assignment():
    assignment_id = request.form.get('assignment_id')
    code = request.form.get('code')

    # Get the assignment
    assignment = Assignment.query.filter_by(assignment_id=assignment_id).first_or_404()

    # Generate the response from the LLM
    llm.generate(assignment.description, code)
    flash('Code submitted successfully!')

    return render_template('assignments/start_assignment.html', assignment=assignment)


@ai_blueprint.route('/create_grade', methods=['GET', 'POST'])
def create_grade():
    assignment_id = request.form.get('assignment_id')
    student_id = request.form.get('student_id')
    grade = 'U'  # U for unmarked
    correct = request.form.get('correct')
    feedback = request.form.get('feedback')
    next_steps = request.form.get('next_steps')
    code_submission = request.form.get('code_submission')

    # Create the grade
    new_grade = Grade(assignment_id=assignment_id,
                      student_id=student_id,
                      grade=grade,
                      correct=correct,
                      feedback=feedback,
                      next_steps=next_steps,
                      code_submission=code_submission)

    # Add to database
    db.session.add(new_grade)
    db.session.commit()

    flash('Grade created successfully!')
    return render_template('grades/grade_assignment.html')