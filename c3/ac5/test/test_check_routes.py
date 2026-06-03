import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from router import check_routes, cargar_tabla_rutas


def ejecutar_pruebas_reales():
    print("Test de enrutamiento\n")
    
    # Definimos los caminos subiendo un nivel antes de entrar a tabla_de_rutas
    ruta_r1 = "tabla_de_rutas/rutas_R1_v2.txt"
    ruta_r2 = "tabla_de_rutas/rutas_R2_v2.txt"
    ruta_r3 = "tabla_de_rutas/rutas_R3_v2.txt"


    # Caso 1: Paquete en R1 con destino final R3 (IP: 127.0.0.1, Puerto: 8883)
    # R1 debe enviarlo a R2 (127.0.0.1, 8882)
    res_r1 = check_routes(ruta_r1, ("127.0.0.1", 8883))
    print(f"R1 buscando destino R3 (8883) -> Siguiente salto: {res_r1}")
    print(f"¿Correcto?: {res_r1 == ('127.0.0.1', 8882)}\n")


    # Caso 2: Paquete en R2 con destino final R1 (IP: 127.0.0.1, Puerto: 8881)
    # R2 debe enviarlo directo a R1 (127.0.0.1, 8881)
    res_r2 = check_routes(ruta_r2, ("127.0.0.1", 8881))
    print(f"R2 buscando destino R1 (8881) -> Siguiente salto: {res_r2}")
    print(f"¿Correcto?: {res_r2 == ('127.0.0.1', 8881)}\n")


    # Caso 3: Paquete en R3 con destino final R1 (IP: 127.0.0.1, Puerto: 8881)
    # R3 debe enviarlo a R2 (127.0.0.1, 8882)
    res_r3 = check_routes(ruta_r3, ("127.0.0.1", 8881))
    print(f"R3 buscando destino R1 (8881) -> Siguiente salto: {res_r3}")
    print(f"¿Correcto?: {res_r3 == ('127.0.0.1', 8882)}\n")


    # Caso 4: Paquete fuera de la red (IP: 127.0.0.1, Puerto: 8884)
    # Ningún router debe encontrar ruta (debe retornar None)
    res_fuera_r1 = check_routes(ruta_r1, ("127.0.0.1", 8884))
    res_fuera_r2 = check_routes(ruta_r2, ("127.0.0.1", 8884))
    print(f"R1 buscando destino inválido (8884) -> Siguiente salto: {res_fuera_r1}")
    print(f"R2 buscando destino inválido (8884) -> Siguiente salto: {res_fuera_r2}")
    print(f"¿Paquete descartado?: {res_fuera_r1 is None and res_fuera_r2 is None}\n")

if __name__ == "__main__":
    ejecutar_pruebas_reales()