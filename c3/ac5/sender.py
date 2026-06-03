import sys
import socket

def create_packet(ip_final, puerto_final, mensaje):
    # Construye el paquete binario con el header de 6 bytes usando el destino final.
    # Codificar la IP (4 bytes)
    componentes_ip = [int(x) for x in ip_final.split('.')]
    ip_bytes = bytes(componentes_ip)
    
    # Codificar el Puerto final (2 bytes, big-endian)
    puerto_bytes = puerto_final.to_bytes(2, byteorder='big')
    mensaje_bytes = mensaje.encode('utf-8')

    return ip_bytes + puerto_bytes + mensaje_bytes

def enviar_paquete():
    # Validar la cantidad de argumentos
    if len(sys.argv) != 6:
        print("Error: Cantidad de argumentos incorrecta.")
        print("Uso: python3 sender.py IP_final puerto_final \"mensaje\" IP_envio puerto_envio")
        sys.exit(1)

    # Asignación y parseo de parámetros
    try:
        ip_final = sys.argv[1]
        puerto_final = int(sys.argv[2])
        mensaje = sys.argv[3]
        ip_envio = sys.argv[4]
        puerto_envio = int(sys.argv[5])
    except ValueError:
        print("Error: Los puertos deben ser números enteros válidos.")
        sys.exit(1)

    # Crear el paquete con la estructura
    paquete_bytes = create_packet(ip_final, puerto_final, mensaje)
    
    # Crear el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # Enviar el paquete hacia la dirección de envío
        sock.sendto(paquete_bytes, (ip_envio, puerto_envio))
        print(f"Paquete enviado con éxito.")
        print(f" -> Destino lógico final encapsulado: {ip_final}:{puerto_final}")
        print(f" -> Destino físico de envío (Next Hop): {ip_envio}:{puerto_envio}")
        print(f" -> Tamaño total: {len(paquete_bytes)} bytes")
    
    except Exception as e:
        print(f"Error al enviar el paquete: {e}")
    
    finally:
        sock.close()






if __name__ == "__main__":
    enviar_paquete()