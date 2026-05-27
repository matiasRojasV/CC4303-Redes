"""
Cliente para test de Go-Back-N sin pérdidas
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from socket_tcp import SocketTCP

IP = '192.168.85.71'
PUERTO = 8000
address = (IP, PUERTO)
switch_mode = 1


client_socketTCP = SocketTCP()
client_socketTCP.connect(address)

modo = "go_back_n" if switch_mode == 1 else "stop_and_wait"

# test archivo 100KB
archivo_100kb = b"B" * (50 * 1024) 

print("Iniciando transmisión de 100KB...")
inicio = time.time()
client_socketTCP.send(archivo_100kb, mode=modo)
fin = time.time()

tiempo_total = fin - inicio
segmentos_totales = client_socketTCP.number_of_sent_segments

print(f"Tiempo de envío: {tiempo_total:.2f} segundos")
print(f"Segmentos enviados: {segmentos_totales}")
