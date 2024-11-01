import requests

def authenticate(username, password):
    url = "https://10.10.20.161/api/v0/authenticate"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "username": username,
        "password": password
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    if response.status_code == 200:
        print("Autenticación exitosa")
        return response.content.decode()
    else:
        print("Error en la autenticación:", response.status_code, response.text)
        return None
