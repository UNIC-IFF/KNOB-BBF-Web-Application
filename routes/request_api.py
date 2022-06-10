"""The Endpoints to manage the Geth Actions"""
import json
import re
import docker
from flask import  abort, request, Blueprint
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


Active_Networks=set()
@GETH_API.route("/request/running_networks", methods=['GET'])
def get_running_networks():
    """Return the available networks"""
    import os 
    #print(os.system("docker stats $(docker ps -q)"))
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    c=client.containers.list(all=True)
    a=[container.name for container in c]  
    if ([i for i in a if i.startswith('xrpl')]):
        Active_Networks.add("xrpl") 
    if ([i for i in a if i.startswith('geth')]):
        Active_Networks.add("geth") 
    if ([i for i in a if i.startswith('besu')]):
        Active_Networks.add("besu-poa") 
    if ([i for i in a if i.startswith('stellar')]):
        Active_Networks.add("stellar")
    return json.dumps(list(Active_Networks))


def control_command(network, command): #
  
    cmd=f" {PATH}/{network}/control.sh {command} "
    session = Popen(['echo {} | sudo -S {}'.format(PWD, cmd)],shell=True, stdout=PIPE, stderr=PIPE)
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
    Active_Networks.remove(str(network))
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

@GETH_API.route('/traffic/<string:network>/traffic', methods=['GET'])
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
    import time
   
    session = Popen([f'cd {cmd} &&   node acc_info.js {public_key}'],shell=True, stdout=PIPE, stderr=PIPE)
 
    stdout, stderr = session.communicate()
    
    print(stdout)
    if stderr:
        print(stderr)
        return json.dumps(stderr.decode('utf-8').replace("'", '"'))
    stdout=stdout.decode('utf-8').replace("'", '"')
    st= stdout.splitlines()
    return json.dumps(st) 
 

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
@GETH_API.route('/docker/managment/stats', methods=['GET'])
#begin with this action for the framework
def docker_stats():
   container_Stats=[]
   client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
   c=client.containers.list(all=True)
   for container in c:
    
    container_Stats.append(container.stats(decode=False,stream=False))
   print(container_Stats)
   return json.dumps(container_Stats)

@GETH_API.route('/docker/managment/list', methods=['GET'])
#returns the container list information
def docker_list():
   client = docker.from_env()
   container_dict=[]
   for container in client.containers.list():
        container_dict.append({"Container_name": container.name,"Container_ID":container.short_id,"Container_status": container.status,"Container_image":re.search(r"\'(.*?)\'",str(container.image)).group(1) })

   return json.dumps(container_dict)