import socket
from socket_tcp import SocketTCP
import sys

IP = '192.168.1.109' # local IPVM
PUERTO = 8000
address = (IP, PUERTO)

# Crear el socket UDP 
server_socketTCP = SocketTCP()
server_socketTCP.bind(address)

# Esperar Handshake del cliente
conn_socket, new_addr = server_socketTCP.accept()

if conn_socket:
    print("\n--- INICIO DEL ARCHIVO RECIBIDO ---\n")
    
    # Recibir los datos usando nuestro Stop & Wait confiable
    while True:
        # Extraemos máximo 16 bytes en cada vuelta
        trozo = conn_socket.recv(16)
        
        # Imprimimos directamente a la salida estándar sin modificar los bytes
        sys.stdout.buffer.write(trozo)
        sys.stdout.flush()
        
        # Condición de salida: Si ya no esperamos más bytes y el buffer está vacío
        if conn_socket.bytes_esperados == 0 and len(conn_socket.buffer_recepcion) == 0:
            break

    print("\n\n--- FIN DEL ARCHIVO ---")
    print(" Recepción completada con éxito.")
    conn_socket.recv_close()
    server_socketTCP.socket_udp.close()
    print("[*] Servidor apagado correctamente.")