import os
import requests
import re
from core.mmlog import get_logger
from core.utils.convert import convert_to_bytes

log = get_logger('__name__')


def check_device_requirement(device_requirement, node_data):
    device_found=False
    for device in node_data.get("devices", {}).values():
        status = device.get("status")
        path = device.get("path")
        #cleaned_path = path.strip("'")
        if (path != None) and (path==device_requirement) and (status=="available"):
            return True
    return device_found

def check_memory_requirement(required_memory, node_data):
    ram = node_data.get("dynamicMetrics", {}).get("freeRAM", 0)
    #ram = node_data.get("staticMetrics", {}).get("RAMMemory", 0)
    mem = convert_to_bytes(required_memory)
    if mem < ram:
        return True
    else:
        return False


def check_cpu_requirement(required_cpus, node_data):
    cpu_cores = node_data.get("staticMetrics", {}).get("cpuCores", 0)
    if cpu_cores>required_cpus:
        return True
    else:
        return False

def check_architecture_requirement(required_arch, node_data):
    architecture = node_data.get("staticMetrics", {}).get("cpuArchitecture")
    if (architecture==required_arch):
        return True
    else:
        return False


def check_component_req_safisfied(component,node_name,node_data):
    ''' Checks if node node_name meets all component requirements '''
     #filtering.py$
    log.info(" In check_component_req_satisfied: component %s node %d node_data %d\n ",component,node_name,node_data)
    #print("\n\nIn check_component_req_satisfied\n")
    #print(component)
    #print(node_name)
    #print(node_data)
    ''' potential_requirements = {
        'memory' : check_memory_requirement(required,node_data),
        'devices': check_device_requirement(required,node_data),
        'cpu': check_cpu_requirement(required,node_data),
        'architecture': check_arquitecture_requirement(required,node_data)
    }'''
    # if there is no requirements they are satisfied
    if 'requirements' not in component:
        return True
    for req_k, req_value, in component['requirements'].items():
        if req_k=='memory':
            if not check_memory_requirement(req_value,node_data):
                return False
        elif req_k=='devices':
            if not check_device_requirement(req_value,node_data):
                return False
        elif req_k=='cpu':
            if not check_cpu_requirement(req_value,node_data):
                return False
        elif req_k=='architecture':
            if not check_architecture_requirement(req_value,node_data):
                return False
        else:
            print("WARNING: Requirement %s has not been implemented yet\n",req_k)
            return False
    # if I get to this point all requirements are satisfied
    return True
            

def filter_candidates(component, taxonomy_json):
    ''' For component component, checks each resource in taxonomy_json meets component requirements '''
     #filtering.py$
    log.info(" In filter_candidates: component %s\n ",component)
    clusters_and_nodes_matching_requirements = []
    for cluster_name, cluster_data in taxonomy_json.get("cluster", {}).items():
        cluster_type = cluster_data.get("type")
        #print ('cluster_type=', cluster_type)
        for node_name, node_data in cluster_data.get("node", {}).items():
            if check_component_req_safisfied(component,node_name,node_data):
                clusters_and_nodes_matching_requirements.append({"cluster_name": cluster_name, "node_name": node_name, "orchestrator": cluster_type})
    return clusters_and_nodes_matching_requirements


def filter_taxonomy_candidates(app_req_components_list ,taxonomy_json):
    ''' It modifies the app_req_components_list to add the candidate targets for each
     component '''
     #filtering.py$
    log.info(" In filter_taxonomy_candidates: %s",app_req_components_list)
    for component in app_req_components_list['components']:
        #print(component)
        #print(type(component))
        component['targets']=filter_candidates(component,taxonomy_json)




