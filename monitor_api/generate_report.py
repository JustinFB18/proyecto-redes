import json
from datetime import datetime

def save_logs(data, filename):
    # Obtener la fecha y hora actual
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato de fecha y hora
    filename = f"reports/{filename}_{current_time}.txt"  # Nombre del archivo con fecha y hora
    
    with open(filename, "w") as file:  # Abrir el archivo en modo escritura
        file.write(f"=== {filename} - {current_time} ===\n")
        file.write(json.dumps(data, indent=4))
        file.write("\n\n")
    
    print(f"Log guardado en {filename}")