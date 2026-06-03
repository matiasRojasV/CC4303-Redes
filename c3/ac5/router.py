import sys
import socket


class RouterState:
    # Mantiene el estado de round-robin para cada área de red.
    def __init__(self):
        # Diccionario: clave = (cidr, puerto_inicio, puerto_final), valor = índice_última_ruta
        self.areas_state = {}
    
    def get_next_route(self, matching_routes: list, area_key: tuple) -> dict:
        # Retorna la siguiente ruta en orden round-robin para un área específica.
        if not matching_routes:
            return None
        
        # Si es la primera vez para esta área, empezar en 0
        if area_key not in self.areas_state:
            self.areas_state[area_key] = 0
        
        # Obtener el índice actual
        current_index = self.areas_state[area_key]
        
        # Seleccionar la ruta
        selected_route = matching_routes[current_index]
        
        # Actualizar el índice (round-robin)
        next_index = (current_index + 1) % len(matching_routes)
        self.areas_state[area_key] = next_index
        
        return selected_route

# Instancia global para mantener estado entre llamadas
_router_state = RouterState()


def cargar_tabla_rutas(archivo_path):
    tabla = []
    try:
        with open(archivo_path, 'r') as archivo:
            for linea in archivo:
                linea = linea.strip()
                # Ignorar líneas vacías o comentarios
                if not linea or linea.startswith('#'):
                    continue
                
                partes = linea.split()
                if len(partes) == 5:
                    ruta = {
                        'cidr': partes[0],
                        'puerto_inicio': int(partes[1]),
                        'puerto_final': int(partes[2]),
                        'ip_gateway': partes[3],
                        'puerto_gateway': int(partes[4])
                    }
                    tabla.append(ruta)
        return tabla

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_path}'")
        sys.exit(1)


def parse_packet(IP_packet: bytes) -> dict:
    # permite extraer los headers y datos del paquete recibido, y lo parsea a una estructura de datos

    # Extraer los 4 bytes de la dirección IP y convertirlos al formato a.b.c.d
    ip_bytes = IP_packet[0:4]
    ip = f"{ip_bytes[0]}.{ip_bytes[1]}.{ip_bytes[2]}.{ip_bytes[3]}"
    
    # Extraer los 2 bytes del puerto y convertirlos a un entero
    puerto_bytes = IP_packet[4:6]
    puerto = int.from_bytes(puerto_bytes, byteorder='big')
    
    # Extraer el bytes del ttl y convertirlos a un entero
    ttl_bytes = IP_packet[6:7]
    ttl = int.from_bytes(ttl_bytes, byteorder='big')

    # Extraer el resto de los bytes correspondientes al mensaje y decodificarlos
    mensaje_bytes = IP_packet[7:]
    mensaje = mensaje_bytes.decode('utf-8')

    # 4. Retornar la estructura de datos conveniente
    return {
        'ip': ip,
        'puerto': puerto,
        'ttl': ttl,
        'mensaje': mensaje
    }


def create_packet(parsed_IP_packet: dict) -> bytes:
    # recibe la estructura de datos de parse_packet y crea un paquete IP de acuerdo a la estructura.

    # Obtener los datos de parsed_IP_packet
    ip = parsed_IP_packet['ip']
    puerto = parsed_IP_packet['puerto']
    ttl = parsed_IP_packet['ttl']
    mensaje = parsed_IP_packet['mensaje']
    
    # Codificar la IP a 4 bytes consecutivos
    componentes_ip = [int(x) for x in ip.split('.')]
    ip_bytes = bytes(componentes_ip)
    
    # Codificar el puerto a 2 bytes (big-endian)
    puerto_bytes = puerto.to_bytes(2, byteorder='big')
    
    # Codificar el ttl a 1 byte
    ttl_bytes = ttl.to_bytes(1, byteorder='big')

    # Codificar el mensaje a bytes
    mensaje_bytes = mensaje.encode('utf-8')
    
    # Concatenar todo para formar el paquete final
    return ip_bytes + puerto_bytes + ttl_bytes + mensaje_bytes


def check_routes(routes_file_name: str, destination_address: tuple[str, int], router_state: RouterState = None)-> tuple[str, int]:
    # Busca rutas en la tabla de enrutamiento y aplica round-robin si hay múltiples opciones.
    dest_ip_str, dest_port = destination_address
    
    # Usar la instancia global si no se proporciona una
    state = router_state if router_state is not None else _router_state
    
    # Validar que la IP de destino sea una dirección IPv4 válida
    tabla_rutas = cargar_tabla_rutas(routes_file_name)
    
    if not tabla_rutas:
        return None

    # Encontrar todas las rutas que coinciden con el destino
    matching_routes = []
    area_key = None
    
    for ruta in tabla_rutas:
        # Usamos split('/')[0] para quedarnos solo con "127.0.0.1" y compararla.
        ip_red = ruta['cidr'].split('/')[0]
        
        # Coincidencia de IP y que el puerto esté en rango
        if dest_ip_str == ip_red and ruta['puerto_inicio'] <= dest_port <= ruta['puerto_final']:
            matching_routes.append(ruta)

            # Crear la clave del área (CIDR, rango de puertos)
            area_key = (ruta['cidr'], ruta['puerto_inicio'], ruta['puerto_final'])
    
    # Si hay al menos una ruta, aplicar round-robin
    if matching_routes:
        selected_route = state.get_next_route(matching_routes, area_key)
        return (selected_route['ip_gateway'], selected_route['puerto_gateway'])
            
    # Retorna None si no hay coincidencias
    return None


def init_router(ip: str, puerto: int, archivo_rutas: str):
    # Configurar el socket de escucha 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, puerto))
    print(f"Servidor router escuchando en {ip}:{puerto}\n")
    
    # Usar la instancia global de estado del router
    router_state = _router_state
    
    # Bucle de escucha
    try:
        while True:
            # Recibir datos del mini-Internet
            datos, direccion_origen = sock.recvfrom(1024)

            # Analizar el paquete binario
            parsed_IP_packet = parse_packet(datos)
            destination_address = (parsed_IP_packet['ip'], parsed_IP_packet['puerto'])
            router_actual = (ip, puerto)

            # El paquete es para este router
            if parsed_IP_packet['ip'] == ip and parsed_IP_packet['puerto'] == puerto:
                print(f"\nPaquete recibido exitosamente en destino final.")
                print(f"Contenido del mensaje: {parsed_IP_packet['mensaje']}\n")

            else:
                next_hop = check_routes(archivo_rutas, destination_address, router_state)

                #obtener el nro del router (DEBUG)
                numero_str = str(puerto)
                if numero_str.startswith('7'):
                    router_num = int(numero_str[0])
                else:
                    router_num = puerto % 10

                if next_hop:
                    # Hacer forward del paquete original en bytes hacia el siguiente salto
                    sock.sendto(datos, next_hop)
                    print(f"\n[{router_num}] redirigiendo paquete hacia {next_hop[1]}")
                else:
                    # Descartar el paquete si check_routes retorna None
                    print(f"No hay rutas hacia {destination_address} para el paquete\n")

    except KeyboardInterrupt:
        print("\nApagando el router...")
    finally:
        sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso correcto: python3 router_roundrobin.py router_IP router_puerto router_rutas.txt")
        sys.exit(1)

    ip_arg = sys.argv[1]
    puerto_arg = int(sys.argv[2])
    archivo_arg = sys.argv[3]

    init_router(ip_arg, puerto_arg, archivo_arg)