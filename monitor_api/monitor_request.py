import requests

def check_system_health(token):
    url = "https://10.10.20.161/api/v0/system_health"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token[1:-1]}"
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print("Consulta de salud del sistema exitosa")
        return response.json()
    else:
        print("Error en la consulta de salud del sistema:", response.status_code, response.text)
        return None

def get_lab_id(token):
    url = "https://10.10.20.161/api/v0/labs"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token[1:-1]}"
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print("Consulta de ID de laboratorio exitosa")
        return response.json()  # Retorna la respuesta completa
    else:
        print("Error en la consulta de ID de laboratorio:", response.status_code, response.text)
        return None
    
def get_lab_nodes_ids(token, lab_id):
    url = f"https://10.10.20.161/api/v0/labs/{lab_id}/nodes?data=false"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token[1:-1]}"
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print("Consulta de nodos del laboratorio exitosa")
        return response.json()  # Retorna la respuesta completa
    else:
        print("Error en la consulta de nodos del laboratorio:", response.status_code, response.text)
        return None
    
def get_lab_state(token, lab_id):
    url = f"https://10.10.20.161/api/v0/labs/{lab_id}/state"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token[1:-1]}"
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        print("Consulta del estado del laboratorio exitosa")
        return response.content.decode()  # Retorna la respuesta completa
    else:
        print("Error en la consulta del estado del laboratorio:", response.status_code, response.text)
        return None

def get_lab_element_state(token, lab_id):
    url = f"https://10.10.20.161/api/v0/labs/{lab_id}/lab_element_state"
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token[1:-1]}'
    }
    
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener el estado del laboratorio {lab_id}: {response.status_code} - {response.text}")
        return None
    
def get_node_information(token, lab_id, node_id):
    url = f"https://10.10.20.161/api/v0/labs/{lab_id}/nodes/{node_id}?simplified=false"
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token[1:-1]}'
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener la información del nodo {node_id}: {response.status_code} - {response.text}")
        return None
    
def get_interfaces_id(token, lab_id, node_id):
    url = f"https://10.10.20.161/api/v0/labs/{lab_id}/nodes/{node_id}/interfaces?data=false"
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token[1:-1]}'
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener la información del ids {node_id}: {response.status_code} - {response.text}")
        return None
    

def get_interfaces_information(token, lab_id, interface_id):
    url = f"https://10.10.20.161/api/v0/labs/{lab_id}/interfaces/{interface_id}"
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token[1:-1]}'
    }

    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener la información del ids {interface_id}: {response.status_code} - {response.text}")
        return None
    
