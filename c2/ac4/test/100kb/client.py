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

# ¡APAGAR el debug para maximizar la velocidad!
client_socketTCP.DEBUG_CC = True 


modo = "go_back_n"

# test archivo 100KB
archivo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archivo_100kb.txt")
with open(archivo_path, "rb") as archivo:
    archivo_100kb = archivo.read()

print("Iniciando transmisión de 100KB...")


tiempos_ejecucion = []

# Guardamos los segmentos al inicio para saber cuántos se enviaron solo en este intento
segmentos_iniciales = client_socketTCP.number_of_sent_segments

inicio = time.time()
client_socketTCP.send(archivo_100kb, mode=modo)
fin = time.time()

tiempo_total = fin - inicio
tiempos_ejecucion.append(tiempo_total)

segmentos_enviados = client_socketTCP.number_of_sent_segments - segmentos_iniciales

print(f"tiempo={tiempo_total:.4f}s, segmentos enviados en este intento={segmentos_enviados}")

# --- Guardar resultados en un archivo de texto ---
resultados_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tiempos_transmision.txt")
with open(resultados_path, "w") as f_out:
    f_out.write("Resultados de la transmisión de 100KB\n")
    f_out.write(f"{tiempo_total:.4f} segundos\n")
    
print(f"\n¡Prueba finalizada! Los tiempos se han guardado en: {resultados_path}")