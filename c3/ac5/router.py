import sys
import socket


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
    
    # Extraer el resto de los bytes correspondientes al mensaje y decodificarlos
    mensaje_bytes = IP_packet[6:]
    mensaje = mensaje_bytes.decode('utf-8')
    
    # 4. Retornar la estructura de datos conveniente
    return {
        'ip': ip,
        'puerto': puerto,
        'mensaje': mensaje
    }


def create_packet(parsed_IP_packet: dict) -> bytes:
    # recibe la estructura de datos de parse_packet y crea un paquete IP de acuerdo a la estructura.

    # Obtener los datos de parsed_IP_packet
    ip = parsed_IP_packet['ip']
    puerto = parsed_IP_packet['puerto']
    mensaje = parsed_IP_packet['mensaje']
    
    # Codificar la IP a 4 bytes consecutivos
    componentes_ip = [int(x) for x in ip.split('.')]
    ip_bytes = bytes(componentes_ip)
    
    # Codificar el puerto a 2 bytes (big-endian)
    puerto_bytes = puerto.to_bytes(2, byteorder='big')
    
    # Codificar el mensaje a bytes
    mensaje_bytes = mensaje.encode('utf-8')
    
    # Concatenar todo para formar el paquete final
    return ip_bytes + puerto_bytes + mensaje_bytes


def check_routes(routes_file_name: str, destination_address: tuple[str, int])-> tuple[str, int]:
    # revisar en orden la tabla de rutas para indicar la dirección del siguiente salto
    dest_ip_str, dest_port = destination_address
    
    # Validar que la IP de destino sea una dirección IPv4 válida
    tabla_rutas = cargar_tabla_rutas(routes_file_name)
    
    if not tabla_rutas:
        return None

    # Recorrer la lista de diccionarios buscando el Gateway
    for ruta in tabla_rutas:
        # Usamos split('/')[0] para quedarnos solo con "127.0.0.1" y compararla.
        ip_red = ruta['cidr'].split('/')[0]
        
        # Coincidencia de IP y que el puerto esté en rango
        if dest_ip_str == ip_red and ruta['puerto_inicio'] <= dest_port <= ruta['puerto_final']:
            return (ruta['ip_gateway'], ruta['puerto_gateway'])
            
    # Retorna None si no hay coincidencias
    return None



def init_router(ip: str, puerto: int, archivo_rutas: str):
    # Bucle principal del router UDP.
    # Configurar el socket de escucha 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
    sock.bind((ip, puerto))
    print(f"Servidor router escuchando en {ip}:{puerto}\n")
    
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
                print(f"Paquete recibido exitosamente en destino final.")
                print(f"Contenido del mensaje: {parsed_IP_packet['mensaje']}\n")

            else:
                next_hop = check_routes(archivo_rutas, destination_address)
                
                if next_hop:
                    # Hacer forward del paquete original en bytes hacia el siguiente salto
                    sock.sendto(datos, next_hop)
                    print(f"redirigiendo paquete con destino final {destination_address} desde {router_actual} hacia {next_hop}\n")
                else:
                    # Descartar el paquete si check_routes retorna None
                    print(f"No hay rutas hacia {destination_address} para paquete {parsed_IP_packet}\n")

    except KeyboardInterrupt:
        print("\nApagando el router...")
    finally:
        sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso correcto: python3 router.py router_IP router_puerto router_rutas.txt")
        sys.exit(1)

    ip_arg = sys.argv[1]
    puerto_arg = int(sys.argv[2])
    archivo_arg = sys.argv[3]

    init_router(ip_arg, puerto_arg, archivo_arg)
    