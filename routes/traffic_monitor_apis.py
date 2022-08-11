import json
from routes.request_api import control_command, compile_network_name
from flask import  abort, jsonify, request, Blueprint
import pandas as pd

NUM_OF_NODES=5
MONITORING_APIS = Blueprint('MONITORING_APIS', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']
INIT_PATH="blockchain-benchmarking-framework/"
OUTPUT_FILE="../output.txt"

def get_blueprint():
    """Return the blueprint for the main app module"""
    return MONITORING_APIS

@MONITORING_APIS.route('/request/mon-stop', methods=['DELETE'])
#begin with this action for the framework
def stop_monitoring():
    
    if request.method == 'DELETE': #configure the monitoring 
        network=""
        return jsonify(control_command(INIT_PATH+"control.sh",network,' -mon prom-monitoring-stack stop',OUTPUT_FILE))
    else:
        abort(404)


@MONITORING_APIS.route('/request/mon', methods=['GET'])
#begin with this action for the framework
def start_monitoring():
    if request.method == 'GET': #configure the monitoring 
        network= " " #the network is not specified in this command 
        check= control_command(INIT_PATH+"control.sh",network,'-mon prom-monitoring-stack configure',OUTPUT_FILE)
        if "error" not in check:
            return jsonify(control_command(INIT_PATH+"control.sh",network,' -mon prom-monitoring-stack start',OUTPUT_FILE))
        else:
            return json.dumps({"Error with configure"})  

@MONITORING_APIS.route('/traffic/<string:network>/traffic/<int:num_of_wallets>/<int:num_of_tokens>', methods=['GET'])
#begin with this action for the framework
def traffic(network,num_of_wallets,num_of_tokens):
    network=compile_network_name(network)
    if network not in BLOCKCHAINS:
             abort(404)            #number_of_wallets  #number_of_tokens
    command = f'./traffic_gen.sh  {num_of_wallets} {num_of_tokens}'
    return jsonify(control_command(INIT_PATH+f"networks/{network}/{network}_traffic_generator/"," ",command,OUTPUT_FILE))
    
@MONITORING_APIS.route('/traffic/<string:network>/node', methods=['GET'])
#begin with this action for the framework
def node(network):
    
    network=compile_network_name(network) #network part
    OUTPUT_FILE="../ouput.txt"
    net=" "
    return jsonify(control_command("cd ~- && cd "+INIT_PATH+f"networks/{network}/{network}_traffic_generator/ && ", net, 'node server_info.js 2> ../../../../ouput.txt && cd ~- ',OUTPUT_FILE))

@MONITORING_APIS.route('/traffic/<string:network>/acc/<string:public_key>', methods=['GET'])
#begin with this action for the framework1
def acc(network,public_key):
    command=f"node acc_info.js {public_key}  2> ../../../../ouput.txt" #traffic part
    OUTPUT_FILE="../ouput.txt"
    return jsonify(control_command("cd ~- && cd  "+INIT_PATH+f"networks/{network}/{network}_traffic_generator/"+' && '," ",command +" && cd ~- ",OUTPUT_FILE))



@MONITORING_APIS.route('/traffic/wallets/<string:network>', methods=['GET'])
#begin with this action for the framework1
def wallets(network):
  path=f' cat blockchain-benchmarking-framework/networks/{network}/{network}_traffic_generator/output_data/accounts_to_pay.txt'
  command=""
  return jsonify(control_command(path," ", " ",OUTPUT_FILE))