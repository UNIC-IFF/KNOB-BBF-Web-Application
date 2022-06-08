"""The Endpoints to manage the Geth Actions"""
import json
from flask import  abort, request, Blueprint
from subprocess import Popen, PIPE
import configparser
from  difflib import get_close_matches as gcm


config = configparser.ConfigParser()
config.read('conf.ini')
PATH= config['DEFAULT']['PATH'] #add your path to framework
PWD= config['DEFAULT']['PWD']#sudo password 

GETH_API = Blueprint('geth_api', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']


def control_command(network, command): #
  
    cmd=f" {PATH}/{network}/control.sh {command} "
    session = Popen(['echo {} | sudo -S {}'.format(PWD, cmd)],shell=True, stdout=PIPE, stderr=PIPE)
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

def compile_network_name(network):
    """Returns the correct folder name for the benchmarking framework"""
    return gcm(network, BLOCKCHAINS)[0]


@GETH_API.route('/request/<string:network>/status', methods=['GET'])
def get_status(network):
    """Return all book requests
    @return: 200: an array of all Nodes and ports as\
    flask/response object with application/json mimetype.
    """
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    st =control_command(network,'status')
    s=[]
    for i in range(4, len(st)-1):
        s.append(st[i])
    return json.dumps(s)

@GETH_API.route('/request/<string:network>/start', methods=['POST'])
def post_start(network):
    """Return all book requests
    @return: 200: an array of all Start logs as a \
    flask/response object with application/json mimetype.
    """
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('Start 5 Nodes') #later we will let the user from the interface to choose this number 
    return json.dumps(control_command(network,'start -n 5'))


@GETH_API.route('/request/<string:network>/clean', methods=['DELETE'])
def clean(network):
    """Return all book requests
    @return: 200: an array of all Start logs as a \
    flask/response object with application/json mimetype.
    """
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('CLEAN') #later we will let the user from the interface to choose this number 
    return json.dumps(control_command(network,'clean'))

@GETH_API.route('/request/<string:network>/configure', methods=['PUT'])
def put_configure(network):
    """Return all book requests
    @return: 200: an array of all Configure logs as a \
    flask/response object with application/json mimetype.
    """
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('Configure 5 Nodes') #later we will let the user from the interface to choose this number 
    return json.dumps(control_command(network,'configure -n 5'))


@GETH_API.route('/request/<string:network>/stop', methods=['DELETE'])
def stop(network):
    """ Stop the Nodes and network    """
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('stop nodes') #later we will let the user from the interface to choose this number with configure
    return json.dumps(control_command(network,'stop'))


@GETH_API.route('/request/<string:network>/mon', methods=['GET', 'POST', 'DELETE'])
#begin with this action for the framework
def monitoring(network):
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    if request.method == 'GET': #configure the monitoring        
        return json.dumps(control_command(network,'-mon prom-monitoring-stack configure')) 
    elif request.method == 'POST': #start the monitoring
        return json.dumps(control_command(network,'-mon prom-monitoring-stack start')) 
    else:
        return json.dumps(control_command(network,'-mon prom-monitoring-stack stop')) 

@GETH_API.route('/request/<string:network>/traffic', methods=['GET'])
#begin with this action for the framework
def traffic(network):
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
             abort(404)
    command = 'traffic_gen.sh  10 1000'
    cmd=f" {PATH}/{network}/{network}_traffic_generator/{command} "
    session = Popen(['echo {} | sudo -S {}'.format(PWD, cmd)],shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    print(stdout)
    if stderr:
        print(stderr)
        return json.dumps(stderr.decode('utf-8').replace("'", '"'))
    stdout=stdout.decode('utf-8').replace("'", '"')
    st= stdout.splitlines()   
    return json.dumps(st) 
    
@GETH_API.route('/request/<string:network>/node', methods=['GET'])
#begin with this action for the framework
def node(network):
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
             abort(404)
    cmd=f" {PATH}/{network}/{network}_traffic_generator"
    session = Popen(['echo server_info.js" | node {}'.format(cmd)],shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    print('echo {} | sudo -S {}'.format(PWD, cmd))
    print(stdout)
    if stderr:
        print(stderr)
        return json.dumps(stderr.decode('utf-8').replace("'", '"'))
    stdout=stdout.decode('utf-8').replace("'", '"')
    st= stdout.splitlines()
    return json.dumps(st) 


