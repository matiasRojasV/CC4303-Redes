import sys
import socket
import os

# Agregar el directorio padre al path para importar router_roundrobin
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from router import create_packet as create_packet_router

def enviar_paquete():
    # Validar la cantidad de argumentos
    if len(sys.argv) != 6:
        print("Error: Cantidad de argumentos incorrecta.")
        print("Uso: python3 sender.py IP_final puerto_final \"mensaje\" IP_envio puerto_envio")
        sys.exit(1)

    # Asignación y parseo de parámetros
 
    ip_final = sys.argv[1]
    puerto_final = int(sys.argv[2])
    mensaje = sys.argv[3]
    ip_envio = sys.argv[4]
    puerto_envio = int(sys.argv[5])


    # Crear el paquete con la estructura
    paquete_bytes = create_packet_router({'ip': ip_final, 'puerto': puerto_final, 'mensaje': mensaje})
    
    # Crear el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Enviar el paquete hacia la dirección de envío
        sock.sendto(paquete_bytes, (ip_envio, puerto_envio))
        print(f"Paquete enviado con éxito.")
    
    except Exception as e:
        print(f"Error al enviar el paquete: {e}")
    
    finally:
        sock.close()


if __name__ == "__main__":
    enviar_paquete()