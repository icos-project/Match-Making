# Here we implement logging functiolality
import os
import json
# MOntse this is not logging I think this is the output?

import logging

# Configure the logger
logging.basicConfig(filename='error.log', level=logging.ERROR)
# logging.basicConfig(filename='nodes_selected.log', level=logging.DEBUG)

def get_logger(name: str):
    log=logging.getLogger(name)
    return log


def save_to_log(nodes_list,app_name):
    log_file_path = "nodes_selected.log"
    
    # Si el archivo no existe, créalo
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as file:
            file.write("")

    # Construir el diccionario con la información requerida
    log_data = {
        app_name: {
            "list_nodes": nodes_list if nodes_list else "none",
            "node_selected": nodes_list[0] if nodes_list else "none"
        }
    }

    # Guardar el diccionario en el archivo de registro
    with open(log_file_path, 'a') as file:
        file.write(json.dumps(log_data, indent=4))
        file.write("\n" + '-'*50 + "\n")

    

