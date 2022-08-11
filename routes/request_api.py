"""The Endpoints to manage the Geth Actions"""
import os
import json
from routes.docker_api import get_running_networks, remove_network
from flask import  abort, Blueprint
from  difflib import get_close_matches as gcm
import pandas as pd
from readerwriterlock import rwlock
import time
import fnmatch

NUM_OF_NODES=5
PATH="blockchain-benchmarking-framework/control.sh "
GETH_API = Blueprint('traffic_api', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']
INIT_PATH="blockchain-benchmarking-framework/ "
OUTPUT_FILE="../output.txt"



def control_command(PATH,network, command, OUTPUT_FILE): #
    # send command to hostpipe
    fi= os.open("../blockchain-benchmarking-framework/bbf-commands", os.O_WRONLY)
    
    lock= rwlock.RWLockFairD()
    lock_w=lock.gen_wlock()
    if lock_w.acquire():
        try:
            os.write(fi,f'{PATH} {network} {command}'.encode())
            #os.write(fi," && ls".encode())
            os.close(fi)
        finally:
            lock_w.release()
    while True:
        if os.path.exists(OUTPUT_FILE):
        
                file1 = os.stat(OUTPUT_FILE) # initial file size
                file1_size = file1.st_size
                time.sleep(0.5)
                file2 = os.stat(OUTPUT_FILE) # updated file size
                file2_size = file2.st_size
                comp = file2_size - file1_size # compares sizes
                if comp == 0:
                    with open(OUTPUT_FILE, 'r') as file:
                        out=file.read().splitlines()
                       
                    break

                else:
                    time.sleep(1)
        else:
            time.sleep(1)
    return out



def get_blueprint():
    """Return the blueprint for the main app module"""
    return GETH_API

def compile_network_name(network):
    """Returns the correct folder name for the benchmarking framework"""
    return gcm(network, BLOCKCHAINS)[0]


@GETH_API.route('/request/<string:network>/path', methods=['GET'])
def path_exists(network):
    dir_path = f'../blockchain-benchmarking-framework/networks/{network}/configfiles/'
    count=5

    if not os.path.exists(f'../blockchain-benchmarking-framework/networks/{network}/docker-compose-testnet.yaml'):
        print("NOT CONFIGURED")
        return json.dumps("NOT CONFIGURED")        
    else:
        dictData = json.loads(get_status(network))
        if any(s for s in dictData["data"]):
            if network == "xrpl":
                count = len(fnmatch.filter(os.listdir(dir_path), f'{network}*')) - 1
            print("Started", count)
            return json.dumps(f"Started, {count}")
        else:
            print("Configured")
            if network == "xrpl":
                count = len(fnmatch.filter(os.listdir(dir_path), f'{network}*'))-1        
            print(os.system("docker stats $(docker ps -q"))
            return json.dumps(f"Configured, {count}")


@GETH_API.route('/request/<string:network>/status', methods=['GET'])
def get_status(network):
    """Return all book requests
    @return: 200: an array of all Nodes and ports as\
    flask/response object with application/json mimetype.
    """
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    st=control_command(PATH,network,'status', OUTPUT_FILE)
    s=[]
    for i in range(3, len(st)-1):
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
    return pd.DataFrame(control_command(PATH,network,f'start -n {NUM_OF_NODES}',OUTPUT_FILE)).to_json(orient='split',indent= 2, index=False)


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
    return pd.DataFrame(control_command(PATH,network,'clean',OUTPUT_FILE)).to_json(orient='split',indent= 2, index=False)

@GETH_API.route('/request/<string:network>/configure/<int:NUM_OF_NODES>', methods=['POST'])
def put_configure(network, NUM_OF_NODES):
    """Return all book requests
    @return: 200: an array of all Configure logs as a \
    flask/response object with application/json mimetype.
    """
    NUM_OF_NODES= abs(NUM_OF_NODES)
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    if network == "besu-poa":
            NUM_OF_NODES_BN= 1
            return pd.DataFrame(control_command(PATH,network,f'configure -bn {NUM_OF_NODES_BN} -vn {NUM_OF_NODES}',OUTPUT_FILE)).to_json(orient='split',indent= 2, index=False) 
    return pd.DataFrame(control_command(PATH,network,f'configure -n {NUM_OF_NODES}', OUTPUT_FILE)).to_json(orient='split',indent= 2, index=False)


@GETH_API.route('/request/<string:network>/configure/<int:NUM_OF_NODES_BN>/<int:NUM_OF_NODES_VN>', methods=['POST'])
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
    return pd.DataFrame(control_command(PATH,network,f'configure -bn {NUM_OF_NODES_BN} -vn {NUM_OF_NODES_VN}',OUTPUT_FILE)).to_json(orient='split',indent= 2, index=False)    


@GETH_API.route('/request/<string:network>/stop', methods=['DELETE'])
def stop(network):
    """ Stop the Nodes and network    """
    
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    print('stop nodes') #later we will let the user from the interface to choose this number with configure
    remove_network(str(network))
    return pd.DataFrame(control_command(PATH,network,'stop',OUTPUT_FILE)).to_json(orient='split',indent= 2, index=False)


@GETH_API.route('/request/list', methods=['GET'])
#begin with this action for the framework
def show_list(): 
    INIT_PATH="blockchain-benchmarking-framework/"+"control.sh -list"
    return pd.DataFrame(control_command(INIT_PATH," ",'--list',OUTPUT_FILE)).to_json(orient='split',indent= 2, index=False)