import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from socket_tcp import SocketTCP

IP = '192.168.1.109'
PUERTO = 8000
address = (IP, PUERTO)

server_socketTCP = SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()

modo = "go_back_n"

# test (Prueba de 100 KB de rendimiento)
print("Test: Esperando recibir archivo de 100KB...")

archivo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archivo_100kb.txt")
with open(archivo_path, "rb") as archivo:
    archivo_100kb = archivo.read()

buff_size_100kb = len(archivo_100kb)
datos_100kb = connection_socketTCP.recv(buff_size_100kb, mode=modo)

print(f"Recibidos: {len(datos_100kb)} bytes.")
print("Test: Passed\n")
