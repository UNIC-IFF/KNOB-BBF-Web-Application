"""The Endpoints to manage the Geth Actions"""
import json
from routes.docker_api import get_running_networks, remove_network
from flask import  abort, Blueprint
from subprocess import Popen, PIPE
import configparser
from  difflib import get_close_matches as gcm
from pathlib import Path

NUM_OF_NODES=5
BASE_PATH = Path(__file__).resolve().parent


config = configparser.ConfigParser()
config.read('conf.ini')
PATH= config['DEFAULT']['PATH'] #add your path to framework
PWD= config['DEFAULT']['PWD']#sudo password 
INIT_PATH= config['DEFAULT']['INIT_PATH']
GETH_API = Blueprint('traffic_api', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']


def control_command(network, command, sudo): #
  
    cmd=f"cd {INIT_PATH} && ./control.sh {network} {command}"
    if sudo == True:
        cmd=f"cd {INIT_PATH} && echo {PWD} | sudo -S ./control.sh {network} {command}"
    print(cmd)
    session = Popen([cmd],shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    print(stdout)
    if stderr:
        print(stderr)
    stdout=stdout.decode('utf-8').replace("'", '"')
    st= stdout.splitlines()
    get_running_networks()
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
    st =control_command(network,'status', sudo=False)
    s=[]
    for i in range(4, len(st)-1):
        s.append(st[i])
    return json.dumps(s)

@GETH_API.route('/request/<string:network>/start/<int:NUM_OF_NODES>', methods=['POST'])
def post_start(network, NUM_OF_NODES):
    """Return all book requests
    @return: 200: an array of all Start logs as a \
    flask/response object with application/json mimetype.
    """
    NUM_OF_NODES= abs(NUM_OF_NODES)
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print(f'Start {NUM_OF_NODES} Nodes') #later we will let the user from the interface to choose this number 
    return json.dumps(control_command(network,f'start -n {NUM_OF_NODES}', sudo=False))


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
    return json.dumps(control_command(network,'clean', sudo=True))

@GETH_API.route('/request/<string:network>/configure/<int:NUM_OF_NODES>', methods=['PUT'])
def put_configure(network, NUM_OF_NODES):
    """Return all book requests
    @return: 200: an array of all Configure logs as a \
    flask/response object with application/json mimetype.
    """
    NUM_OF_NODES= abs(NUM_OF_NODES)
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('Configure 5 Nodes') #later we will let the user from the interface to choose this number 
    return json.dumps(control_command(network,f'configure -n {NUM_OF_NODES}', sudo=False))


@GETH_API.route('/request/<string:network>/stop', methods=['DELETE'])
def stop(network):
    """ Stop the Nodes and network    """
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('stop nodes') #later we will let the user from the interface to choose this number with configure
    remove_network(str(network))
    return json.dumps(control_command(network,'stop', sudo=False))


@GETH_API.route('/request/list', methods=['GET'])
#begin with this action for the framework
def show_list():
    
    cmd=INIT_PATH+"control.sh -list"
    session = Popen(['echo | {}'.format( cmd)],shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        print(stderr)
        abort(404)
    stdout=stdout.decode('utf-8').splitlines()     
    return json.dumps(stdout) 