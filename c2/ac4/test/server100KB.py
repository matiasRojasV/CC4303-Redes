"""
Test de Go-Back-N sin pérdidas
Verifica que send/recv con mode="go_back_n" funciona correctamente
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socket_tcp import SocketTCP

IP = '192.168.85.71'
PUERTO = 8000
address = (IP, PUERTO)
switch_mode = 1

server_socketTCP = SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()

modo = "go_back_n" if switch_mode == 1 else "stop_and_wait"

# test (Prueba de 100 KB de rendimiento)
print("Test: Esperando recibir archivo de 100KB...")
 
connection_socketTCP.socket_udp.settimeout(20.0)

# 100 KB = 100 * 1024 bytes = 102400 bytes
TEST_5_BYTES = 100 * 1024
buff_size_100kb = TEST_5_BYTES 

datos_100kb = connection_socketTCP.recv(buff_size_100kb, mode=modo)

print(f"Test recibidos: {len(datos_100kb)} bytes.")
if len(datos_100kb) == TEST_5_BYTES:
    print("Test: Passed\n")
else:
    print("Test: Failed\n")
