"""
Cliente para test de Go-Back-N sin pérdidas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socket_tcp import SocketTCP

IP = '192.168.1.109'
PUERTO = 8000
address = (IP, PUERTO)
switch_mode = 1



# ============ CLIENT ============
print("CLIENTE - Go-Back-N")


client_socketTCP = SocketTCP()
client_socketTCP.connect(address)
print(f"Conectado a {IP}:{PUERTO}\n")


if switch_mode == 1:
    modo = "go_back_n"
else:
    modo = "stop_and_wait"

# test 1
print("[Test 1] Enviando mensaje de 16 bytes...")
message = "Mensje de len=16".encode()
print(f"  Mensaje: {message}")
client_socketTCP.send(message, mode=modo)
print("  ✓ Enviado\n")

# test 2
print("[Test 2] Enviando mensaje de 19 bytes...")
message = "Mensaje de largo 19".encode()
print(f"  Mensaje: {message}")
client_socketTCP.send(message, mode=modo)
print("  ✓ Enviado\n")

# test 3
print("[Test 3] Enviando mensaje de 19 bytes...")
message = "Mensaje de largo 19".encode()
print(f"  Mensaje: {message}")
client_socketTCP.send(message, mode=modo)
print("  ✓ Enviado\n")

print("[Cierre] Cerrando conexión...")
client_socketTCP.close()


print("CLIENTE FINALIZADO")

