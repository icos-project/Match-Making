#This file implements functionality to extract requirements from the Application Descriptor
import yaml
import json
import httpx
import os
import requests
import re

def extract_resources(appdesc_json):
    return appdesc_json[0]['components']
    

def extract_cpu_value(cpu_string):
    if type(cpu_string) == str:
        value = float(cpu_string[:-1])
        value *= 0.001
        return value
    else:
        return float(cpu_string)

def extract_architecture(image_name):
    # Utilizamos una expresión regular para extraer la arquitectura después del ":"
    match = re.search(r':([^/]+)$', image_name)
    if match:
        return match.group(1)
    else:
        return None

