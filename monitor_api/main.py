import os
from auth_request import authenticate
import monitor_request as monitor
import generate_report as report

def get_state_info(token, lab_id):
    lab_status = monitor.get_lab_state(token, lab_id)
    if lab_status:
        print(f"Estado del laboratorio {lab_id}:", lab_status)

    elements_lab_status = monitor.get_lab_element_state(token, lab_id)
    if elements_lab_status:
        print(f"Estado de los elementos del laboratorio {lab_id} obtenidos exitosamente")

    combined_data = {
        "lab_id": lab_id,
        "lab_status": elements_lab_status 
    }

    # Guardar el estado en un archivo .txt
    report.save_logs(combined_data, f"lab_state_{lab_id}")

def main():
    username = "developer"
    password = "C1sco12345"
    
    # Autenticar y obtener token
    token = authenticate(username, password)
    if not token:
        print("No se pudo autenticar. Terminando el programa.")
        return

    health_response = monitor.check_system_health(token)
    if health_response:
        print("Datos de salud del sistema:", health_response)
        # Guardar en el archivo de logs
        report.save_logs(health_response, "health_response")

    # Obtener el ID del laboratorio
    lab_ids_list = monitor.get_lab_id(token)

    if lab_ids_list:
        print("Datos del laboratorio:", lab_ids_list)

        for lab_id in lab_ids_list:  # Iterar sobre la lista de IDs de laboratorios
            os.makedirs(str(f"reports/lab_info_{lab_id}"), exist_ok=True)

            nodes_data = monitor.get_lab_nodes_ids(token, lab_id)
            if nodes_data:
                print("Datos de nodos del laboratorio:", nodes_data)

            # Obtener el estado del laboratorio
            get_state_info(token, lab_id)

            for node_id in nodes_data:
                node_status = monitor.get_node_information(token, lab_id, node_id)
                interfaces_ids = monitor.get_interfaces_id(token, lab_id, node_id)
                if node_status:
                    print(f"Estado del nodo {node_id} obtenidos exitosamente")
                # Guardar el estado en un archivo .txt
                report.save_logs_dir(node_status, os.path.join(str(f"reports/lab_info_{lab_id}")), f"node_state_{node_id}")

                for interface_id in interfaces_ids:
                    interface_status = monitor.get_interfaces_information(token, lab_id, interface_id)
                    if interface_status:
                        print(f"Estado de la interfaz {interface_id} del nodo {node_id} obtenidos exitosamente")
                    # Guardar el estado en un archivo .txt
                    report.save_logs_dir(interface_status, os.path.join(str(f"reports/lab_info_{lab_id}")), f"interface_state_{interface_id}")


if __name__ == "__main__":
    main()
