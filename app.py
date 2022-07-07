"""A Python Flask REST API BoilerPlate (CRUD) Style"""
import argparse
import os
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS
from flask_babel import gettext
from flask_swagger_ui import get_swaggerui_blueprint
from routes import request_api, traffic_monitor_apis, docker_api
from flask_babel import Babel



APP = Flask(__name__)
APP.app_context().push()
CORS(APP)
Babel(APP)
### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Blockchain-Benchmarking-Framework-Flask-API"
    }
)

@APP.route("/home", methods=["GET", "POST"])
def home():
    return render_template('home.html')
@APP.route("/home1", methods=["GET", "POST"])
def home1():
    return render_template('home1.html')

@APP.route("/blog", methods=["GET", "POST"])
def blog():
    return render_template('blog.html')

@APP.route("/token", methods=["GET", "POST"])
def token():
    return render_template('token.html')


@APP.route("/ico", methods=["GET", "POST"])
def ico():
    li=request_api.show_list()
    return render_template('ico.html')


@APP.route("/roadmap", methods=["GET", "POST"])
def roadmap():
    return render_template('roadmap.html')

@APP.route("/dozzle", methods=["GET", "POST"])
def dozzle():
    return render_template('dozzle.html') 

@APP.route("/grafana", methods=["GET", "POST"])
def grafana():
    return render_template('grafana.html')      

    

APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


APP.register_blueprint(request_api.get_blueprint())
APP.register_blueprint(traffic_monitor_apis.get_blueprint())
APP.register_blueprint(docker_api.get_blueprint())

@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Blockchain Benchmarking Framework Flask API")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 5000))

    APP.run(host='0.0.0.0', port=PORT, debug=True, extra_files=['./static/swagger.json'])
