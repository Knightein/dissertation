import flask
from flask import render_template

error_blueprint = flask.Blueprint(
    'error', __name__, template_folder="templates")


# Error Handlers
@error_blueprint.app_errorhandler(400)
def bad_request(error):
    print("400 Bad Request Error")
    return render_template('error/400.html'), 400


@error_blueprint.app_errorhandler(403)
def forbidden_error(error):
    print("403 Forbidden Error")
    return render_template('error/403.html'), 403


@error_blueprint.app_errorhandler(404)
def notfound_error(error):
    print("404 Not Found Error")
    return render_template('error/404.html'), 404


@error_blueprint.app_errorhandler(500)
def internal_server_error(error):
    print("500 Internal Server Error")
    return render_template('error/500.html'), 500


@error_blueprint.app_errorhandler(503)
def service_error(error):
    print("503 Service Unavailable Error")
    return render_template('error/503.html'), 503
