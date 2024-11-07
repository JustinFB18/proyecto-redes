import json
import os
from datetime import datetime
import re
from prettytable import PrettyTable
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def parse_node_data(filename):
    with open(f"{filename}", "r") as f:
        lines = f.readlines()
    
    lines.pop(0)  # Eliminar la primera línea

    json_string = ''.join(lines)  # Combinar el resto de líneas en un string

    data = json.loads(json_string)  # Cargar el JSON en un diccionario
    
    # Convertir el diccionario al formato solicitado
    # formatted_data = f"label: {data['label']}\n"
    # formatted_data += f"node_definition: {data['node_definition']}\n"
    # formatted_data += f"state: {data['state']}\n"
    # formatted_data += f"image_definition: {data['image_definition']}\n"
    # formatted_data += f"ram: {data['ram']}\n"
    

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
                if filename.startswith("interface_state_") and filename.endswith(".txt"):
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
    table.field_names = ["Label", "Slot", "State", "Is Connected?", "nodeID", "Timestamp"]
    table.align = "l"  # Left align for readability
    table.max_width = 20  # Set a width if needed to avoid line breaks

    # Display or process the most recent files for each node_id
    for node_id, info in latest_files.items():
        # Parse file to get data fields
        node_data = parse_node_data(info['file_path'])

        connection_status = f"{GREEN}True{RESET}" if node_data["is_connected"] else f"{RED}False{RESET}"
        
        
        # Add row to table
        table.add_row([
            node_data["label"],
            node_data["slot"],
            f"{BLUE}{node_data['state']}{RESET}",  # Blue color for "State"
            connection_status,
            node_id,
            info['file_time']
        ])

    # Print the table
    print(table)
    return table

def convert_table_to_pdf(data, headers=None, output_filename="table_output.pdf"):
    """
    Convierte una lista de datos en una tabla en un archivo PDF.
    
    :param data: Lista de filas de la tabla (cada fila es una lista de celdas).
    :param headers: Opcional. Una lista de encabezados de columna.
    :param output_filename: Nombre del archivo PDF de salida.
    """
    # Crear un objeto canvas para el PDF
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter  # Tamaño de la página

    # Establecer la posición inicial de la tabla
    y_position = height - 40  # Inicia cerca de la parte superior
    padding = 10  # Espaciado entre celdas
    column_widths = [100, 100, 100, 100, 100, 100]  # Ancho de las columnas (ajustar según el contenido)

    # Dibujar encabezados de la tabla
    if headers:
        x_position = 40  # Posición inicial horizontal
        for i, header in enumerate(headers):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x_position, y_position, header)
            x_position += column_widths[i] + padding  # Ajustar posición horizontal

        y_position -= 20  # Baja para la siguiente fila

    # Dibujar las filas de la tabla
    c.setFont("Helvetica", 10)  # Fuente para las filas de datos
    for row in data:
        x_position = 40  # Posición inicial horizontal
        for i, cell in enumerate(row):
            c.drawString(x_position, y_position, str(cell))
            x_position += column_widths[i] + padding  # Ajustar posición horizontal

        y_position -= 20  # Baja para la siguiente fila

        if y_position < 40:  # Si llega al final de la página, crea una nueva página
            c.showPage()
            y_position = height - 40  # Reiniciar posición vertical

    # Guardar el PDF
    c.save()
    print(f"PDF guardado como {output_filename}")

headers = ["Label", "Slot", "State", "Is Connected?", "nodeID", "Timestamp"]

# Call the function to process all node response files
parse_all_nodes_response()
convert_table_to_pdf(data, headers, "node_report.pdf")