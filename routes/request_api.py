"""The Endpoints to manage the Geth Actions"""
from concurrent.futures import process
import os
from routes.docker_api import get_running_networks, remove_network
from flask import  abort, Blueprint
from subprocess import Popen, PIPE
import configparser
from  difflib import get_close_matches as gcm
from pathlib import Path
import pandas as pd
import multiprocessing

NUM_OF_NODES=5
BASE_PATH = Path(__file__).resolve().parent


config = configparser.ConfigParser()
config.read('conf.ini')
PATH= config['DEFAULT']['PATH'] #add your path to framework
PWD= config['DEFAULT']['PWD']#sudo password 
INIT_PATH= config['DEFAULT']['INIT_PATH']
GETH_API = Blueprint('traffic_api', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']


def get_char(process):
    character = process.stdout
    print(
        character,
        end="",
        flush=True,  # Unbuffered print
    )
    return character

def search_for_output(strings, process):
    buffer = ""
    while not any(string in buffer for string in strings):
        buffer = buffer + get_char(process)

def control_command(network, command, sudo): #
    f= os.open("blockchain-benchmarking-framework/bbf-commands", os.O_RDWR)

    
    cmd=f"echo blockchain-benchmarking-framework/control.sh xrpl status"
    if sudo == True:
        cmd=f"cd {INIT_PATH} && echo {PWD} | sudo -S ./control.sh {network} {command}"
    process = Popen([cmd],shell=True,stdin=PIPE, stdout=f, stderr=PIPE)
    #ps_process = Popen([cmd], stdout=f)
    grep_process = Popen(['cat blockchain-benchmarking-framework/bbf-commands'], shell= True,stdin=f, stdout=PIPE)
    output = grep_process.communicate()[0]
    
    print(output)
    #if stderr:
    #    print(stderr)
    #stdout=stdout.decode('utf-8').replace("'", '"').splitlines()
    #get_running_networks
    return "stdout"



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
    st=control_command(network,'status', sudo=False)
    s=[]
    for i in range(4, len(st)-1):
        s.append(st[i])
    return pd.DataFrame(s).to_json(orient='split',indent= 2, index=False)

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
    return pd.DataFrame(control_command(network,f'start -n {NUM_OF_NODES}', sudo=False)).to_json(orient='split',indent= 2, index=False)


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
    return pd.DataFrame(control_command(network,'clean', sudo=True)).to_json(orient='split',indent= 2, index=False)

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
    return pd.DataFrame(control_command(network,f'configure -n {NUM_OF_NODES}', sudo=False)).to_json(orient='split',indent= 2, index=False)


@GETH_API.route('/request/<string:network>/configure/<int:NUM_OF_NODES_BN>/<int:NUM_OF_NODES_VN>', methods=['PUT'])
def put_configure_besu(network, NUM_OF_NODES_BN, NUM_OF_NODES_VN):
    """Return all book requests
    @return: 200: an array of all Configure logs as a \
    flask/response object with application/json mimetype.
    """
    NUM_OF_NODES_BN= abs(NUM_OF_NODES_BN)
    NUM_OF_NODES_VN=abs(NUM_OF_NODES_VN)
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('Configure 5 Nodes') #later we will let the user from the interface to choose this number 
    return pd.DataFrame(control_command(network,f'configure -bn {NUM_OF_NODES_BN} -vn {NUM_OF_NODES_VN}', sudo=False)).to_json(orient='split',indent= 2, index=False)    


@GETH_API.route('/request/<string:network>/stop', methods=['DELETE'])
def stop(network):
    """ Stop the Nodes and network    """
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('stop nodes') #later we will let the user from the interface to choose this number with configure
    remove_network(str(network))
    return pd.DataFrame(control_command(network,'stop', sudo=False)).to_json(orient='split',indent= 2, index=False)


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
    return pd.DataFrame(stdout).to_json(orient='split',indent= 2, index=False) 