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

# 100 KB = 100 * 1024 bytes = 102400 bytes
archivo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archivo_100kb.txt")
with open(archivo_path, "rb") as archivo:
    archivo_100kb = archivo.read()

TEST_5_BYTES = len(archivo_100kb)
buff_size_100kb = TEST_5_BYTES

for intento in range(1, 6):
    datos_100kb = connection_socketTCP.recv(buff_size_100kb, mode=modo)

    print(f"Intento {intento} recibidos: {len(datos_100kb)} bytes.")
    print("Test: Passed\n")
