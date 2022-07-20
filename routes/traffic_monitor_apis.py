import json
import re
from routes.request_api import control_command, compile_network_name
from flask import  abort, jsonify, request, Blueprint
import pandas as pd

NUM_OF_NODES=5
MONITORING_APIS = Blueprint('MONITORING_APIS', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']
INIT_PATH="blockchain-benchmarking-framework/"

def get_blueprint():
    """Return the blueprint for the main app module"""
    return MONITORING_APIS

@MONITORING_APIS.route('/request/<string:network>/mon', methods=['GET', 'POST', 'DELETE'])
#begin with this action for the framework
def monitoring(network):
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
         abort(404)
    if request.method == 'GET': #configure the monitoring 
        network= " " #the network is not specified in this command      
        return json.dumps(control_command(INIT_PATH+"control.sh",network,'-mon prom-monitoring-stack configure')) 
    elif request.method == 'POST': #start the monitoring
        network= " " #the network is not specified in this command 
        check= control_command(INIT_PATH+"control.sh",network,'-mon prom-monitoring-stack configure')
        if "error" not in check:
            return json.dumps(control_command(INIT_PATH+"control.sh",network,'-mon prom-monitoring-stack start'))
        else:
            abort(404)
            return json.dumps({"Error with configure"})
    else:
        return json.dumps(control_command(INIT_PATH+"control.sh",network,'-mon prom-monitoring-stack stop')) 

@MONITORING_APIS.route('/traffic/<string:network>/traffic/<int:num_of_nodes>/<int:num_of_txs>', methods=['GET'])
#begin with this action for the framework
def traffic(network,num_of_nodes,num_of_txs):
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
             abort(404)
    command = f'./traffic_gen.sh  {num_of_nodes} {num_of_txs}'
    return pd.DataFrame(control_command(INIT_PATH+f"networks/{network}/{network}_traffic_generator/"," ",command)).to_json(orient='split',indent= 2, index=False)
    
@MONITORING_APIS.route('/traffic/<string:network>/node', methods=['GET'])
#begin with this action for the framework
def node(network):
    
    network=compile_network_name(network)
    return pd.DataFrame(control_command(INIT_PATH+f"networks/{network}/{network}_traffic_generator/"," ",'node server_info.js')).to_json(orient='split',indent= 2, index=False)

@MONITORING_APIS.route('/traffic/<string:network>/acc/<string:public_key>', methods=['POST'])
#begin with this action for the framework
def acc(network,public_key):
    command=f"node acc_info.js {public_key}"
    return pd.DataFrame(control_command(INIT_PATH+f"networks/{network}/{network}_traffic_generator/"," ",command)).to_json(orient='split',indent= 2, index=False)

 