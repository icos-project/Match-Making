import yaml
import json
from core.mmlog import get_logger

log = get_logger('matchmake')


# Function to convert YAML to JSON
def read_yaml_file(yaml_file):
    log.info('Read yaml file: %s',yaml_file)
    try:
        with open(yaml_file, 'r') as yml_file:
            data = yaml_to_json_list(yml_file)
            return data  
    except Exception as e:
        log.error('Failed reading yaml file %s: %s', yaml_file, str(e))
        return None
''        #raise HTTPException(status_code=500, detail=f'Error converting the file: {e}')

# Function to convert validate YAML str
def validate_yaml_body(yaml_content: str):
    try:
        data = yaml.safe_load(yaml_content)  
        return data  
    except Exception as e:
        log.error('Failed converting yaml file to Json: %s', str(e))
        return None
        #raise HTTPException(status_code=500, detail=f'Error converting YAML to JSON: {e}')
    
# Function to convert YAML to JSON
def yaml_to_json_list(yaml_content: str):
    log.info('Reading list of yamls to json format: %s',yaml_content)
    try:
        data = list(yaml.safe_load_all(yaml_content))
        return data
    except Exception as e:
        log.error('Failed converting yaml list of files to Json: %s', str(e))
        return None
        #raise HTTPException(status_code=500, detail=f'Error converting YAML to JSON: {e}')

def read_agregator_file(file_name):
    log.info('Reading  aggregator file: %s',file_name)
    with open(file_name, 'r') as file:
        agregator_json = json.load(file)
    return agregator_json
