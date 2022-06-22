import json
import re
import docker
from flask import   Blueprint
import configparser
from pathlib import Path
import datetime
import pandas as pd


NUM_OF_NODES=5
BASE_PATH = Path(__file__).resolve().parent
config = configparser.ConfigParser()
config.read('conf.ini')
PATH= config['DEFAULT']['PATH'] #add your path to framework
PWD= config['DEFAULT']['PWD']#sudo password 
INIT_PATH= config['DEFAULT']['INIT_PATH']
GETH_API = Blueprint('docker_api', __name__)
BLOCKCHAINS= ['geth', 'xrpl', 'besu-poa', 'stellar-docker-testnet']

Active_Networks=set()
def remove_network(network):
    Active_Networks.remove(network)


def normalize(dictionary): # transforms docker output to dict
    for key, value in dictionary.items():
        if isinstance(value, dict):
            normalize(value)

        item_dict = dict()
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "op" in item:
                    item_dict.update({item.pop("op"): item})
        if item_dict:
            dictionary[key] = item_dict

    return dictionary


def get_blueprint():
    """Return the blueprint for the main app module"""
    return GETH_API



@GETH_API.route("/docker/managment/running_networks", methods=['GET'])
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


@GETH_API.route('/docker/managment/stats', methods=['GET'])
#begin with this action for the framework
def docker_stats():
   container_Stats=[]
   client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
   c=client.containers.list()
   #for container in c:
   # container_Stats.append(container.stats(decode=False,stream=False))
   stats= {str(c1.name): c1.stats(decode=False, stream=False) for c1 in c}
   stats = normalize(stats)
   print(stats)
   for i in stats.values():
     if "manager" not in i['name']:
      # --------------------------- CPU STATS ----------------------------
      UsageDelta = i['cpu_stats']['cpu_usage']['total_usage'] - i['precpu_stats']['cpu_usage']['total_usage']
      SystemDelta= i['cpu_stats']['system_cpu_usage'] - i['precpu_stats']['system_cpu_usage']
      len_cpu = len(i['cpu_stats']['cpu_usage']['percpu_usage'])
      percent = round((UsageDelta / SystemDelta) * len_cpu * 100,3)

      # --------------------------- Memory STATS -------------------------

      memory_usage = i["memory_stats"]["usage"] - i["memory_stats"]["stats"]["cache"]
      limit = i["memory_stats"]["limit"]
      memory_utilization = round(memory_usage/limit * 100, 3)
     #--------------------------- UpTime ----------------------------------
      date= (pd.to_datetime(datetime.datetime.now(datetime.timezone.utc))-pd.to_datetime(i['read']))
      
      container_Stats.append({"Container_name":i['name'], "Network_Stats":i['networks'], "memory_usage_percentage":memory_utilization, "CPU_ucsage_percent":percent, "Uptime":str(date)})
     else:
            continue

   return json.dumps(container_Stats)



@GETH_API.route('/docker/managment/list', methods=['GET'])
#returns the container list information
def docker_list():
   client = docker.from_env()
   container_dict=[]
   for container in client.containers.list():
        container_dict.append({"Container_name": container.name,"Container_ID":container.short_id,"Container_status": container.status,"Container_image":re.search(r"\'(.*?)\'",str(container.image)).group(1) })

   return json.dumps(container_dict)

def docker_logs():
   import io

   client = docker.from_env()
   container_logs={}
   for container in client.containers.list():
    a =pd.DataFrame(container.logs(timestamps=False,tail=40).decode("utf8").splitlines(), index=None, columns=None)
    container_logs[container.name]= a.to_html(header=False,index=False, table_id="table-logs", classes="table-striped table-dark table-responsive w-100 d-block d-md-table")
   return  container_logs