



class socketTCP:
    def __init__(self):
        return True
    

    @staticmethod
    def parse_segment():
        # parsea segmentos TCP a una estructura de datos
        return True
    

    @staticmethod
    def create_segment():
        # crea segmentos a partir de una estructura de datos.
        return True
    

    def bind(address: str) -> None:
        # Funcion que se encarga de que el objeto 
        # socketTCP escuche en la dirección address.
        return True
    

    def connect(address: str) -> None:
        # Funcion que inicia la conexión desde un objeto 
        # socketTCP con otro que se encuentra escuchando 
        # en la dirección address
        return True
    

    def accept():
        # Funcion que se encuentra esperando una petición 
        # de tipo SYN. Dentro de esta funcion deberá implementar 
        # el lado del servidor del 3-way handshake.
        return True
    

    def send(msg):
        # Funcion encargada de manejar Stop & Wait 
        # desde el lado del emisor
        return True
    

    def recv(buff_size):
        return True
    

    def close():
        return True
    
    def recv_close():
        return True

        

    
