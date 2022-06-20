import json
from routes.request_api import control_command, compile_network_name
from flask import  abort, jsonify, request, Blueprint
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
GETH_API = Blueprint('geth_api', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']

def get_blueprint():
    """Return the blueprint for the main app module"""
    return GETH_API

@GETH_API.route('/request/<string:network>/mon', methods=['GET', 'POST', 'DELETE'])
#begin with this action for the framework
def monitoring(network):
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    if request.method == 'GET': #configure the monitoring 
        network= " " #the network is not specified in this command      
        return json.dumps(control_command(network,'-mon prom-monitoring-stack configure',sudo=False)) 
    elif request.method == 'POST': #start the monitoring
        network= " " #the network is not specified in this command  
        return json.dumps(control_command(network,'-mon prom-monitoring-stack start',sudo=False)) 
    else:
        return json.dumps(control_command(network,'-mon prom-monitoring-stack stop',sudo=False)) 

@GETH_API.route('/traffic/<string:network>/traffic/<int:num_of_nodes>/<int:num_of_txs>', methods=['GET'])
#begin with this action for the framework
def traffic(network,num_of_nodes,num_of_txs):
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
             abort(404)
    command = f'./traffic_gen.sh  {num_of_nodes} {num_of_txs}'
    cmd=f"{PATH}/{network}/{network}_traffic_generator/ && echo {PWD} | sudo -S {command}  "
    print (cmd)
    session = Popen(['cd '+cmd],shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    print(type(stdout))
    if stderr:
        print(stderr)
        return json.dumps(stderr.decode('utf-8'))
    stdout=stdout.decode('utf8').replace("'", '"')
    s = json.loads(stdout)

    return json.dumps(stdout) 
    
@GETH_API.route('/traffic/<string:network>/node', methods=['GET'])
#begin with this action for the framework
def node(network):
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
             abort(404)
    cmd=f"{PATH}/{network}/{network}_traffic_generator/"
    session = Popen([f'cd {cmd} &&   node server_info.js'],shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    print(stdout)
    if stderr:
        print(stderr)
        return json.dumps(stderr.decode('utf-8').replace("'", '"'))
    stdout=stdout.decode('utf-8').replace("'", '"')
    st= stdout.splitlines()
    return json.dumps(st)

@GETH_API.route('/traffic/<string:network>/acc/<string:public_key>', methods=['POST'])
#begin with this action for the framework
def acc(network,public_key):
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
             abort(404)
    cmd=f"{PATH}/{network}/{network}_traffic_generator/"
   
    session = Popen([f'cd {cmd} &&   node acc_info.js {public_key}'],shell=True, stdout=PIPE, stderr=PIPE)
 
    stdout, stderr = session.communicate()
    
    print(stdout)
    if stderr:
        print(stderr)
        return json.dumps(stderr.decode('utf-8').replace("'", '"'))
    stdout=stdout.decode('utf-8').replace("'", '"')
    st= stdout.splitlines()
    return json.dumps(st) 
 