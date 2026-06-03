import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socket_tcp import SocketTCP

IP = '192.168.1.109'
PUERTO = 8000
address = (IP, PUERTO)
EDGE_MESSAGE_BYTES = 256

client_socketTCP = SocketTCP()
client_socketTCP.connect(address)
modo = "go_back_n"

# test 1
message = "Mensje de len=16".encode('utf-8')
client_socketTCP.send(message, mode=modo)

# test 2
message = "Mensaje de largo 19".encode('utf-8')
client_socketTCP.send(message, mode=modo)

# test 3
message = "Mensaje de largo 19".encode('utf-8')
client_socketTCP.send(message, mode=modo)

# test 4 (caso borde)
message = bytes([i % 256 for i in range(EDGE_MESSAGE_BYTES)])
client_socketTCP.send(message, mode=modo)