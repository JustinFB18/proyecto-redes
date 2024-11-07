import json
import os
from datetime import datetime
import re
from prettytable import PrettyTable

BLUE = '\033[94m'
RESET = '\033[0m'

def parse_node_data(filename):
    with open(f"{filename}", "r") as f:
        lines = f.readlines()
    
    lines.pop(0)  # Eliminar la primera línea

    json_string = ''.join(lines)  # Combinar el resto de líneas en un string

    data = json.loads(json_string)  # Cargar el JSON en un diccionario
    
    # Convertir el diccionario al formato solicitado
    formatted_data = f"label: {data['label']}\n"
    formatted_data += f"node_definition: {data['node_definition']}\n"
    formatted_data += f"state: {data['state']}\n"
    formatted_data += f"image_definition: {data['image_definition']}\n"
    formatted_data += f"ram: {data['ram']}\n"
    

    #print(formatted_data)

    return data  # Devuelve el diccionario para el resumen

def parse_all_nodes_response():
    directory_pattern = r'reports/lab_info_.*'  # Pattern for directories to search
    base_directory = 'reports'  # Base directory for listing
    regex = re.compile(directory_pattern)

    latest_files = {}  # Dictionary to store the most recent file for each node_id

    # Iterate over directories in the base directory
    for entry in os.listdir(base_directory):
        directory = os.path.join(base_directory, entry)
        
        if os.path.isdir(directory) and regex.match(directory):
            for filename in os.listdir(directory):
                # Check if the filename matches "node_state_" and ends with ".txt"
                if filename.startswith("node_state_") and filename.endswith(".txt"):
                    file_path = os.path.join(directory, filename)
                    
                    # Extract date, time, and node_id from filename
                    date_part, time_part = filename.split("_")[-2], filename.split("_")[-1].replace(".txt", "")
                    node_id = filename.split("_")[2]
                    full_time_str = f"{date_part}_{time_part}"
                    file_time = datetime.strptime(full_time_str, "%Y-%m-%d_%H-%M-%S")
                    
                    # If this node_id is new or has a more recent file, update the dictionary
                    if node_id not in latest_files or file_time > latest_files[node_id]['file_time']:
                        latest_files[node_id] = {
                            'file_path': file_path,
                            'file_time': file_time
                        }

    # Prepare a table with headers
    table = PrettyTable()
    table.field_names = ["Label", "NodeDefinition", "State", "ImageDefinition", "RAM", "nodeID", "Timestamp"]
    table.align = "l"  # Left align for readability
    table.max_width = 20  # Set a width if needed to avoid line breaks

    # Display or process the most recent files for each node_id
    for node_id, info in latest_files.items():
        # Parse file to get data fields
        node_data = parse_node_data(info['file_path'])
        
        # Add row to table
        table.add_row([
            node_data["label"],
            node_data["node_definition"],
            f"{BLUE}{node_data['state']}{RESET}",  # Blue color for "State"
            node_data["image_definition"],
            node_data["ram"],
            node_id,
            info['file_time']
        ])

    # Print the table
    #print(table)
    return table.get_html_string()

# Call the function to process all node response files
parse_all_nodes_response()