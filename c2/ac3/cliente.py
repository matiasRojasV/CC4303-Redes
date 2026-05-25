import sys
from socket_tcp import SocketTCP

IP_DESTINO = '192.168.1.109'

# Validar que se pasen los argumentos correctos
if len(sys.argv) != 3:
    print("Uso correcto: python3 cliente.py <ip> <puerto> < archivo.txt")
    sys.exit(1)

#IP_DESTINO = sys.argv[1]

PUERTO_DESTINO = int(sys.argv[2])
address = (IP_DESTINO, PUERTO_DESTINO)

# Creamos el socket e iniciar Handshake
client_socket = SocketTCP()
client_socket.connect(address)

if client_socket.conectado:
    # Leemos todos los bytes que entran por el archivo direccionado con '<'
    print("[*] Leyendo datos del archivo...")
    datos_archivo = sys.stdin.buffer.read()
    
    # Enviamos todo usando nuestro método confiable (que lo pica de a 16)
    print(f"[*] Enviando un total de {len(datos_archivo)} bytes...")
    client_socket.send(datos_archivo)
    print(" Envío completado con éxito.")
    client_socket.close()
    print("[*] Cliente finalizado correctamente.")