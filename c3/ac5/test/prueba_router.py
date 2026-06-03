import sys
import socket
import time
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from router import create_packet
def main():
    # 1. Validar que se entreguen los argumentos correctos
    if len(sys.argv) != 4:
        print("Uso correcto: python3 prueba_router.py <headers> <IP_router_inicial> <puerto_router_inicial>")
        print("Ejemplo: python3 prueba_router.py 127.0.0.1;8885;10 127.0.0.1 8881")
        sys.exit(1)

    # 2. Parsear los argumentos
    headers = sys.argv[1].split(';')
    if len(headers) != 3:
        print("Error: Los headers deben tener el formato IP;PUERTO;TTL")
        sys.exit(1)
        
    ip_destino = headers[0]
    puerto_destino = int(headers[1])
    ttl = int(headers[2])
    
    ip_router_inicial = sys.argv[2]
    puerto_router_inicial = int(sys.argv[3])

    # 3. Configurar el socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 4. Leer el archivo línea por línea 
    print(f"Enviando tráfico al router {ip_router_inicial}:{puerto_router_inicial}...")
    print(f"Destino final: {ip_destino}:{puerto_destino} (TTL: {ttl})\n")
    
    # Leemos línea por línea
    for linea in sys.stdin:
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue
            
        # Encapsulamos la línea con los headers
        diccionario_paquete = {
            'ip': ip_destino,
            'puerto': puerto_destino,
            'ttl': ttl,
            'mensaje': linea_limpia
        }   

        paquete_bytes = create_packet(diccionario_paquete)
        # Enviamos el paquete al router inicial
        sock.sendto(paquete_bytes, (ip_router_inicial, puerto_router_inicial))
        print(f"Enviado: {linea_limpia}")
        # Pausa opcional recomendada para no saturar los buffers UDP
        time.sleep(0.05)
        
    sock.close()
    print("Envío finalizado.")

if __name__ == "__main__":
    main()