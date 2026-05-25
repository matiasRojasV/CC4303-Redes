"""
Test de Go-Back-N sin pérdidas
Verifica que send/recv con mode="go_back_n" funciona correctamente
"""

import sys
import os
import socket
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socket_tcp import SocketTCP

IP = '192.168.1.109'
PUERTO = 8000
address = (IP, PUERTO)
switch_mode = 1



# ============ SERVER ============
print("SERVIDOR - Go-Back-N")


server_socketTCP = SocketTCP()
server_socketTCP.bind(address)
print(f"Servidor escuchando en {IP}:{PUERTO}...\n")

connection_socketTCP, new_address = server_socketTCP.accept()
print(f"Cliente conectado desde {new_address}\n")

if switch_mode == 1:
    modo = "go_back_n"
else:
    modo = "stop_and_wait"

# test 1: Mensaje exacto de 16 bytes
print("[Test 1] Recibiendo mensaje de 16 bytes...")
buff_size = 16
full_message = connection_socketTCP.recv(buff_size, mode=modo)
print(f"  Recibido: {full_message}")
if full_message == "Mensje de len=16".encode():
    print("  ✓ Test 1: PASSED\n")
else:
    print("  ✗ Test 1: FAILED\n")

# test 2: Mensaje de 19 bytes de una sola lectura
print("[Test 2] Recibiendo mensaje de 19 bytes...")
buff_size = 19
full_message = connection_socketTCP.recv(buff_size, mode=modo)
print(f"  Recibido: {full_message}")
if full_message == "Mensaje de largo 19".encode():
    print("  ✓ Test 2: PASSED\n")
else:
    print("  ✗ Test 2: FAILED\n")

# test 3: Mensaje de 19 bytes en dos lecturas (buff_size=14)
# Esto prueba que recv() acumula correctamente cuando buff_size < message_length
print("[Test 3] Recibiendo mensaje de 19 bytes en dos llamadas...")
print("  Primera lectura (buff_size=14)...")
buff_size = 14
message_part_1 = connection_socketTCP.recv(buff_size, mode=modo)
print(f"    Parte 1: {message_part_1} (len={len(message_part_1)})")

print("  Segunda lectura (buff_size=14)...")
message_part_2 = connection_socketTCP.recv(buff_size, mode=modo)
print(f"    Parte 2: {message_part_2} (len={len(message_part_2)})")

full_message_3 = message_part_1 + message_part_2
print(f"  Mensaje completo: {full_message_3}")
if full_message_3 == "Mensaje de largo 19".encode():
    print("  ✓ Test 3: PASSED\n")
else:
    print("  ✗ Test 3: FAILED\n")

print("[Cierre] Esperando cierre del cliente...")
connection_socketTCP.recv_close()


print("SERVIDOR FINALIZADO")

