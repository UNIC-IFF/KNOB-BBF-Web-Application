"""The Endpoints to manage the Geth Actions"""
from pathlib import Path

import json
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from subprocess import Popen, PIPE
from validate_email import validate_email
GETH_API = Blueprint('geth_api', __name__)


def control_command(command): #
    pwd='1234' #sudo password is required for the time being
    cmd=str(Path.home())+'/Documents/blockchain-benchmarking-framework/networks/geth/control.sh ' + command
    session = Popen(['echo {} | sudo -S {}'.format(pwd, cmd)],shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    print(stdout)
    if stderr:
        print(stderr)
    stdout=stdout.decode('utf-8').replace("'", '"')
    st= stdout.splitlines()
    
    return st

def get_blueprint():
    """Return the blueprint for the main app module"""
    return GETH_API



@GETH_API.route('/request/status', methods=['GET'])
def get_status():
    """Return all book requests
    @return: 200: an array of all Nodes and ports as\
    flask/response object with application/json mimetype.
    """
    st =control_command('status')
    s=[]
    for i in range(4, len(st)-1):
        s.append(st[i])
    return json.dumps(s)

@GETH_API.route('/request/start', methods=['POST'])
def post_start():
    """Return all book requests
    @return: 200: an array of all Start logs as a \
    flask/response object with application/json mimetype.
    """
    print('Start 10 Nodes') #later we will let the user from the interface to choose this number 
    return json.dumps(control_command('start -n 10'))

@GETH_API.route('/request/configure', methods=['PUT'])
def put_configure():
    """Return all book requests
    @return: 200: an array of all Configure logs as a \
    flask/response object with application/json mimetype.
    """
    print('Configure 10 Nodes') #later we will let the user from the interface to choose this number 
    return json.dumps(control_command('configure -n 10'))


@GETH_API.route('/request/stop', methods=['DELETE'])
def geth_stop():
    """ Stop the Nodes and network    """
    print('stop nodes') #later we will let the user from the interface to choose this number with configure
    return json.dumps(control_command('stop'))


@GETH_API.route('/request/mon', methods=['GET', 'POST'])
#begin with this action for the framework
def monitoring():
    if request.method == 'GET': #configure the monitoring        
        return json.dumps(control_command('-mon prom-monitoring-stack configure')) 
    else: #start the monitoring
        return json.dumps(control_command('-mon prom-monitoring-stack start')) 


