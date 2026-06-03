import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socket_tcp import SocketTCP

IP = '192.168.1.109'
PUERTO = 8000
address = (IP, PUERTO)
EDGE_MESSAGE_BYTES = 256

server_socketTCP = SocketTCP()
server_socketTCP.bind(address)
connection_socketTCP, new_address = server_socketTCP.accept()
modo = "go_back_n"

# test 1
buff_size = 16
full_message = connection_socketTCP.recv(buff_size, mode=modo)
print("Test 1 received:", full_message)
if full_message == "Mensje de len=16".encode('utf-8'):
    print("Test 1: Passed\n")
else:
    print("Test 1: Failed\n")

# test 2
buff_size = 19
full_message = connection_socketTCP.recv(buff_size, mode=modo)
print("Test 2 received:", full_message)
if full_message == "Mensaje de largo 19".encode('utf-8'):
    print("Test 2: Passed\n")
else:
    print("Test 2: Failed\n")

# test 3
buff_size = 14
message_part_1 = connection_socketTCP.recv(buff_size, mode=modo)
message_part_2 = connection_socketTCP.recv(buff_size, mode=modo)
print("Test 3 received:", message_part_1 + message_part_2)
if (message_part_1 + message_part_2) == "Mensaje de largo 19".encode('utf-8'):
    print("Test 3: Passed\n")
else:
    print("Test 3: Failed\n")

# test 4 (caso borde): retrasar ACKs para forzar timeout y disminucion de ventana
print("Test 4: Edge case - delaying ACKs...")
time.sleep(2)
buff_size = 128
received = bytearray()

while len(received) < EDGE_MESSAGE_BYTES:
    received += connection_socketTCP.recv(buff_size, mode=modo)

expected = bytes([i % 256 for i in range(EDGE_MESSAGE_BYTES)])
print("Test 4 received bytes:", len(received))
if received == expected:
    print("Test 4: Passed\n")
else:
    print("Test 4: Failed\n")


