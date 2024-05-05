from datetime import datetime

import bcrypt

from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_user, login_required, current_user, logout_user
from markupsafe import Markup

from app import db
from users.forms import RegisterForm, LoginForm
from models import User, required_roles

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # Authentication Attempts
    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0

    # Check limit
    if session.get('authentication_attempts') >= 3:
        flash(Markup('Too many login attempts. Please try again later.'
                     '<br> Please click <a href="/reset">Here</a> to reset!'))
        return render_template('users/login.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists
        if user:
            # Check if password is correct using bcrypt
            if bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
                # Log user in
                login_user(user)
                user.last_login = user.current_login
                user.current_login = datetime.now()
                db.session.add(user)
                db.session.commit()

                # Check if user is a teacher
                if user.role == 'teacher':
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('index'))
            else:
                # Increment authentication attempts
                session['authentication_attempts'] += 1
                # Important to not give away information about what was incorrect
                flash('Incorrect email or password. Please try again.')
                return render_template('users/login.html', form=form)
        else:
            # Increment authentication attempts
            session['authentication_attempts'] += 1
            # Likewise here
            flash('Incorrect email or password. Please try again.')
            return render_template('users/login.html', form=form)

    return render_template('users/login.html', form=form)


@users_blueprint.route('/reset')
def reset():
    # Reset the authentication attempts]
    session['authentication_attempts'] = 0
    return redirect(url_for('users.login'))


@users_blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # Create Form
    form = RegisterForm()

    # Validate Form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # If user exists already
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # Create new user
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        password=form.password.data,
                        role='student')

        # Add to DB
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))

    # If request is GET or form is invalid render the register page
    return render_template('users/register.html', form=form)
