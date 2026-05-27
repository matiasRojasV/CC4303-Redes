import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from socket_tcp import SocketTCP

IP = '192.168.1.109'
PUERTO = 8000
address = (IP, PUERTO)

client_socketTCP = SocketTCP()
client_socketTCP.connect(address)

modo = "go_back_n"

# test archivo 100KB
archivo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archivo_100kb.txt")
with open(archivo_path, "rb") as archivo:
	archivo_100kb = archivo.read()

print("Iniciando transmisión de 100KB...")
for intento in range(1, 6):
	inicio = time.time()
	client_socketTCP.send(archivo_100kb, mode=modo)
	fin = time.time()

	tiempo_total = fin - inicio
	segmentos_totales = client_socketTCP.number_of_sent_segments

	print(f"Intento {intento}: tiempo={tiempo_total:.2f}s, segmentos={segmentos_totales}")
