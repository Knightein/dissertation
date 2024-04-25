from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


# CONFIG
app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'long_and_super_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diss_db.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB
db = SQLAlchemy(app)


# HOME PAGE
@app.route('/')
def index():  # put application's code here
    return render_template('main/index.html')


# BLUEPRINTS
from error.errors import error_blueprint
from assignments.views import assignments_blueprint
from users.views import users_blueprint
from ai.views import ai_blueprint
from grades.views import grades_blueprint

app.register_blueprint(error_blueprint)
app.register_blueprint(assignments_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(ai_blueprint)
app.register_blueprint(grades_blueprint)

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


# Avoid Cycle Imports
from models import User


# Load user with given ID
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.debug = True
    app.run()
