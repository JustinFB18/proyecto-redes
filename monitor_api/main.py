from auth_request import authenticate
import monitor_request as monitor
import generate_report as report

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

        # Obtener los nodos del laboratorio
        for lab_id in lab_ids_list:  # Iterar sobre la lista de IDs de laboratorios
            nodes_data = monitor.get_lab_nodes(token, lab_id)
            if nodes_data:
                print("Datos de nodos del laboratorio:", nodes_data)
            
            lab_status = monitor.get_lab_state(token, lab_id)
            if lab_status:
                print(f"Estado del laboratorio {lab_id}:", lab_status)

            elements_lab_status = monitor.get_lab_element_state(token, lab_id)
            if elements_lab_status:
                print(f"Estado del laboratorio {lab_id}:", elements_lab_status)
                
                combined_data = {
                    "lab_id": lab_id,
                    "lab_status": elements_lab_status 
                }
                
                # Guardar el estado en un archivo .txt
                report.save_logs(combined_data, f"lab_state_{lab_id}")

            

if __name__ == "__main__":
    main()
