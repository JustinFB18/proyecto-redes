import json
import os
from datetime import datetime

def parse_health_response(filename):
    with open(f"{filename}.txt", "r") as f:
        lines = f.readlines()

    print(lines[0])  # Imprimir la primera línea que se eliminará
    lines.pop(0)  # Eliminar la primera línea

    json_string = ''.join(lines)  # Combinar el resto de líneas en un string

    data = json.loads(json_string)  # Cargar el JSON en un diccionario

    # Convertir el diccionario al formato solicitado
    formatted_data = f"Valid: {data['valid']}\n"
    formatted_data += "computes:\n"
    for idx, (comp_id, comp_data) in enumerate(data['computes'].items(), start=1):
        formatted_data += f"    {idx}. id: {comp_id}\n"
        for key, value in comp_data.items():
            formatted_data += f"       {key}: {value}\n"

    formatted_data += f"is_licensed: {data['is_licensed']}\n"
    formatted_data += f"is_enterprise: {data['is_enterprise']}\n"
    formatted_data += "controller:\n"
    for key, value in data['controller'].items():
        formatted_data += f"    {key}: {value}\n"

    print(formatted_data)

    return data  # Devuelve el diccionario para el resumen

def parse_all_health_response():
    directory = 'reports'  # Carpeta donde buscar los archivos
    error_summary = []  # Lista para acumular errores
    last_file_status = "Ok"  # Estado del archivo más reciente
    last_file_name = ""  # Nombre del archivo más reciente
    last_file_time = None  # Tiempo del archivo más reciente

    for filename in os.listdir(directory):
        if filename.startswith("health_response") and filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            file_time_str = filename.split("_")[-1].replace(".txt", "")  # Extraer la parte de fecha y hora
            file_date_str = filename.split("_")[2]  # Extraer la parte de fecha
            
            # Combinar la fecha y hora
            full_time_str = f"{file_date_str}_{file_time_str}"
            file_time = datetime.strptime(full_time_str, "%Y-%m-%d_%H-%M-%S")  # Convertir a objeto datetime

            # Procesar el archivo
            data = parse_health_response(file_path[0:-4])

            # Verificar valores y acumular errores
            if not data['valid']:
                error_summary.append(f"{filename}: Validación fallida")
                last_file_status = "Not Ok"  # Marcamos el archivo como No Ok
            if not data['is_licensed']:
                error_summary.append(f"{filename}: No tiene licencia")
                last_file_status = "Not Ok"
            if not data['is_enterprise']:
                error_summary.append(f"{filename}: No es de tipo enterprise")
                last_file_status = "Not Ok"
            for comp_id, comp_data in data['computes'].items():
                for key, value in comp_data.items():
                    if key != 'id' and not value:  # Ignorar 'id', verificar el resto
                        error_summary.append(f"{filename}: {key} es False")
                        last_file_status = "Not Ok"

            # Verificar si es el archivo más reciente
            if last_file_time is None or file_time > last_file_time:
                last_file_time = file_time
                last_file_name = filename  # Guardar el nombre del archivo más reciente
                last_file_status = "Ok" if last_file_status == "Ok" else "Not Ok"

    print("="*70)
    # Imprimir el resumen de errores
    if error_summary:
        print("\nResumen de Errores:")
        for error in error_summary:
            print(error)
    else:
        print("\nNo se encontraron errores en los archivos.")

    # Indicar el estado del último archivo
    if last_file_status=="Not Ok":
        print(f"\nÚltima respuesta de salud: {last_file_name} - {last_file_status}")
    else:
        print(f"\nÚltima respuesta de salud: {last_file_name} - {last_file_status}")
    print("="*70)

# Llamar a la función para procesar todos los archivos de respuesta de salud
parse_all_health_response()
