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



client_socketTCP = SocketTCP()
client_socketTCP.connect(address)

modo = "go_back_n" if switch_mode == 1 else "stop_and_wait"

# test 1
message = "Mensje de len=16".encode()
client_socketTCP.send(message, mode=modo)

# test 2
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message, mode=modo)

# test 3
message = "Mensaje de largo 19".encode()
client_socketTCP.send(message, mode=modo)

