import socket
import struct
import random

class SocketTCP:
    def __init__(self):
        # Socket UDP
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.direccion_origen = None
        self.direccion_destino = None
        self.seq_num_esperado = 0
        self.seq_num_a_enviar = 0
        self.TIMEOUT = 1.0
        self.MAX_PAYLOAD = 16
        self.conectado = False
        self.bytes_esperados = 0
        self.buffer_recepcion = b""
        

    @staticmethod
    def create_segment(data, seq_num, syn=0, ack=0, fin=0):
        """
        Crea un segmento binario: [Header (2 bytes)] + [Data (N bytes)]
        Flags: SYN (bit 0), ACK (bit 1), FIN (bit 2)
        """
        # Empaquetamos las banderas en un solo byte
        flags = (syn << 0) | (ack << 1) | (fin << 2)
        
        # '!' indica orden de red (Big-Endian)
        # 'B' indica Unsigned Char (1 byte)
        # Formato: 1 byte para seq_num, 1 byte para flags
        header = struct.pack('!BB', seq_num, flags)
        
        # Retornamos la unión del encabezado con los datos en bytes
        return header + data


    @staticmethod
    def parse_segment(segment_bytes):
        """
        Desarma el segmento binario y devuelve un diccionario con los campos.
        """
        header_size = 2
        header = segment_bytes[:header_size]
        payload = segment_bytes[header_size:]
        
        # Desempaquetamos los dos bytes del encabezado
        seq_num, flags = struct.unpack('!BB', header)
        
        # Extraemos cada bandera
        return {
            'seq_num': seq_num,
            'syn': (flags >> 0) & 1,
            'ack': (flags >> 1) & 1,
            'fin': (flags >> 2) & 1,
            'data': payload
        }


    def bind(self, address):
        """Asocia el socket UDP a una dirección y puerto local."""
        self.socket_udp.bind(address)
        self.direccion_origen = address
        print(f"[SocketTCP] Escuchando (bind) en {address}")


    def connect(self, address):
        self.direccion_destino = address
        seq_x = random.randint(0, 100)
        segmento_syn = self.create_segment(b"", seq_num=seq_x, syn=1, ack=0, fin=0)
        self.socket_udp.settimeout(self.TIMEOUT)
        while True:
            self.socket_udp.sendto(segmento_syn, self.direccion_destino)
            try:
                msg_recibido, nueva_direccion_servidor = self.socket_udp.recvfrom(1024)
                segmento_recibido = self.parse_segment(msg_recibido)
                
                if segmento_recibido['syn'] == 1 and segmento_recibido['ack'] == 1:
                    seq_y = segmento_recibido['seq_num']
                    self.direccion_destino = nueva_direccion_servidor
                    
                    # Enviar ACK final y salir 
                    ack_seg = self.create_segment(b"", seq_num=seq_y, syn=0, ack=1, fin=0)
                    self.socket_udp.sendto(ack_seg, self.direccion_destino)
                    
                    self.seq_num_a_enviar = 0
                    self.seq_num_esperado = 0
                    self.conectado = True
                    self.socket_udp.settimeout(None)
                    return
            except socket.timeout:
                # Si no llega el SYN-ACK, repetimos el bucle
                continue


    def accept(self):
        self.socket_udp.settimeout(None) 
        
        while True:
            msg_recibido, direccion_cliente = self.socket_udp.recvfrom(1024)
            segmento_recibido = self.parse_segment(msg_recibido)
            
            if segmento_recibido['syn'] == 1:
                seq_x = segmento_recibido['seq_num']
                
                nuevo_socket = SocketTCP()
                nuevo_socket.bind((self.direccion_origen[0], 0))
                nuevo_socket.direccion_destino = direccion_cliente
                
                seq_y = random.randint(0, 100)
                segmento_syn_ack = nuevo_socket.create_segment(b"", seq_num=seq_y, syn=1, ack=1, fin=0)

                nuevo_socket.socket_udp.settimeout(self.TIMEOUT)

                while True:
                    nuevo_socket.socket_udp.sendto(segmento_syn_ack, direccion_cliente)
                    try:
                        msg_ack, _ = nuevo_socket.socket_udp.recvfrom(1024)
                        segmento_ack = nuevo_socket.parse_segment(msg_ack)
                        
                        if segmento_ack['ack'] == 1 and segmento_ack['syn'] == 0:
                            nuevo_socket.seq_num_a_enviar = 0
                            nuevo_socket.seq_num_esperado = 0
                            nuevo_socket.conectado = True
                            nuevo_socket.socket_udp.settimeout(None)
                            return nuevo_socket, nuevo_socket.direccion_origen
                            
                    except socket.timeout:
                        # Si se pierde el ACK final, repetimos el bucle y retransmitimos SYN-ACK
                        continue


    def _enviar_confiable(self, payload):
        segmento = self.create_segment(payload, self.seq_num_a_enviar, syn=0, ack=0, fin=0)
        self.socket_udp.settimeout(self.TIMEOUT)
        
        while True:
            self.socket_udp.sendto(segmento, self.direccion_destino)
            try:
                msg_ack, _ = self.socket_udp.recvfrom(1024)
                ack_segmento = self.parse_segment(msg_ack)

                # Si recibimos un SYN-ACK mientras enviamos datos, el Servidor está atascado.
                if ack_segmento['syn'] == 1 and ack_segmento['ack'] == 1:
                    print("\n[Stop&Wait] SYN-ACK atrasado detectado. Reenviando ACK del Handshake.")
                    ack_seg = self.create_segment(b"", ack_segmento['seq_num'], syn=0, ack=1, fin=0)
                    self.socket_udp.sendto(ack_seg, self.direccion_destino)
                    continue 
                
                if ack_segmento['ack'] == 1 and ack_segmento['syn'] == 0 and ack_segmento['seq_num'] == self.seq_num_a_enviar:
                    self.socket_udp.settimeout(None)
                    self.seq_num_a_enviar = 1 - self.seq_num_a_enviar
                    break                 
            except socket.timeout:
                continue


    def send(self, message):
        """Divide el mensaje en fragmentos y los envía confiablemente."""
        # Envia el primer paquete especial, el largo total del mensaje
        largo_msg_bytes = str(len(message)).encode('utf-8')
        print(f"[Send] Avisando al receptor que se enviarán {len(message)} bytes.")
        self._enviar_confiable(largo_msg_bytes)
        
        # Envia el mensaje real en trozos de máximo 16 bytes
        for i in range(0, len(message), self.MAX_PAYLOAD):
            trozo = message[i:i+self.MAX_PAYLOAD]
            self._enviar_confiable(trozo)


    def _recibir_confiable(self):
        self.socket_udp.settimeout(None)
        
        while True:
            msg_recibido, addr = self.socket_udp.recvfrom(1024)
            segmento = self.parse_segment(msg_recibido)
            
            if segmento['syn'] == 1 and segmento['ack'] == 1:
                print("\n[Stop&Wait] SYN-ACK atrasado detectado. Reenviando ACK del Handshake.")
                ack_seg = self.create_segment(b"", segmento['seq_num'], syn=0, ack=1, fin=0)
                self.socket_udp.sendto(ack_seg, addr)
                continue
                
            if segmento['seq_num'] == self.seq_num_esperado and segmento['syn'] == 0 and segmento['ack'] == 0:
                ack_seg = self.create_segment(b"", self.seq_num_esperado, syn=0, ack=1, fin=0)
                self.socket_udp.sendto(ack_seg, addr)
                self.seq_num_esperado = 1 - self.seq_num_esperado
                return segmento['data']
                
            elif segmento['syn'] == 0 and segmento['ack'] == 0:
                # Es un dato duplicado, reenviamos su ACK
                ack_seg = self.create_segment(b"", segmento['seq_num'], syn=0, ack=1, fin=0)
                self.socket_udp.sendto(ack_seg, addr)


    def recv(self, buff_size):
        """Acumula los paquetes recibidos y entrega la cantidad solicitada."""
        if self.bytes_esperados == 0 and len(self.buffer_recepcion) == 0:
            data_largo = self._recibir_confiable()
            self.bytes_esperados = int(data_largo.decode('utf-8'))
            print(f"[Recv] Se espera recibir un mensaje de {self.bytes_esperados} bytes.")
            
        bytes_a_entregar_ahora = min(self.bytes_esperados, buff_size)
        
        while len(self.buffer_recepcion) < bytes_a_entregar_ahora:
            data = self._recibir_confiable()
            self.buffer_recepcion += data
            
        datos_retorno = self.buffer_recepcion[:bytes_a_entregar_ahora]
        
        # Guardamos en el buffer lo que sobre para la próxima vez que llamen a recv()
        self.buffer_recepcion = self.buffer_recepcion[bytes_a_entregar_ahora:]
        self.bytes_esperados -= len(datos_retorno)       
        return datos_retorno


    def close(self):
        """
        Implementa el cierre desde el lado de "Host A" tolerando pérdidas.
        Espera los paquetes ACK y FIN correspondientes retransmitiendo si es necesario.
        """
        print("\n[Close - Host A] Iniciando cierre de conexión...")
        segmento_fin = self.create_segment(b"", self.seq_num_a_enviar, syn=0, ack=0, fin=1)
        self.socket_udp.settimeout(self.TIMEOUT)      
        ack_recibido = False
        fin_recibido = False
        intentos = 0
        direccion_b = self.direccion_destino
        ultimo_seq_b = 0
        
        self.socket_udp.sendto(segmento_fin, self.direccion_destino)
    
        while intentos < 3 and (not ack_recibido or not fin_recibido):
            try:
                msg_recibido, addr = self.socket_udp.recvfrom(1024)
                segmento = self.parse_segment(msg_recibido)
                direccion_b = addr
                
                # Registramos si nos llegó el ACK a nuestro FIN
                if segmento['ack'] == 1 and not ack_recibido:
                    print("[Close - Host A] ACK recibido de Host B.")
                    ack_recibido = True
                
                # Registramos si nos llegó el FIN de Host B
                if segmento['fin'] == 1 and not fin_recibido:
                    print("[Close - Host A] FIN recibido de Host B.")
                    fin_recibido = True
                    ultimo_seq_b = segmento['seq_num']
                    
            except socket.timeout:
                intentos += 1
                print(f"[Close - Host A] Timeout {intentos}/3 esperando respuestas (ACK/FIN). Reenviando FIN...")
                if intentos < 3:
                    self.socket_udp.sendto(segmento_fin, self.direccion_destino)
                    
        # Esto si salimos del ciclo por límite de timeouts sin recibir todo
        if not (ack_recibido and fin_recibido):
            print("[Close - Host A] Se cumplió el tercer timeout sin respuestas completas.")
            self.conectado = False
            self.socket_udp.close()
            return
            
        print("[Close - Host A] ¡Respuestas recibidas con éxito! Mitigando pérdidas del último ACK...")
        ack_final = self.create_segment(b"", ultimo_seq_b, syn=0, ack=1, fin=0)
        
        import time
        for i in range(3):
            self.socket_udp.sendto(ack_final, direccion_b)
            print(f"[Close - Host A] ACK final enviado ({i+1}/3). Esperando un timeout...")
            if i < 2: 
                time.sleep(self.TIMEOUT)
            
        self.conectado = False
        self.socket_udp.close()
        print("[Close - Host A] ¡Conexión y recursos liberados exitosamente!")


    def recv_close(self):
        """
        Implementa el cierre desde el lado de "Host B" tolerando pérdidas.
        Espera el último ACK un máximo de 3 timeouts antes de abandonar.
        """
        print("\n[Recv Close - Host B] Esperando petición de cierre (FIN)...")
        self.socket_udp.settimeout(None)        
        direccion_host_a = None
        seq_host_a = 0
        
        # Esperar el paquete FIN inicial del Host A
        while True:
            msg_recibido, addr = self.socket_udp.recvfrom(1024)
            segmento_fin_a = self.parse_segment(msg_recibido)
            
            if segmento_fin_a['fin'] == 1:
                print("[Recv Close - Host B] FIN recibido. Enviando ACK...")
                direccion_host_a = addr
                seq_host_a = segmento_fin_a['seq_num']
                
                # Enviamos el ACK confirmando que procesamos su FIN
                ack_seg = self.create_segment(b"", seq_host_a, syn=0, ack=1, fin=0)
                self.socket_udp.sendto(ack_seg, direccion_host_a)
                break
                
        # Enviamos nuestro propio paquete FIN y esperamos el ACK final con manejo de pérdidas
        print("[Recv Close - Host B] Enviando FIN al Host A...")
        segmento_fin_b = self.create_segment(b"", self.seq_num_a_enviar, syn=0, ack=0, fin=1)
        self.socket_udp.settimeout(self.TIMEOUT)    
        intentos = 0
        ack_final_recibido = False
        
        self.socket_udp.sendto(segmento_fin_b, direccion_host_a)
        
        while intentos < 3:
            try:
                msg_recibido, _ = self.socket_udp.recvfrom(1024)
                ack_final = self.parse_segment(msg_recibido)
                
                if ack_final['ack'] == 1:
                    print("[Recv Close - Host B] ACK final recibido con éxito.")
                    ack_final_recibido = True
                    break
            except socket.timeout:
                intentos += 1
                print(f"[Recv Close - Host B] Timeout {intentos}/3 esperando el ACK final. Reenviando FIN...")
                if intentos < 3:
                    self.socket_udp.sendto(segmento_fin_b, direccion_host_a)
                    
        if not ack_final_recibido:
            print("[Recv Close - Host B] Tercer timeout alcanzado sin ACK final. Asumiendo que Host A cerró.")
            
        # Cerrar recursos 
        self.conectado = False
        self.socket_udp.close()
        print("[Recv Close - Host B] ¡Conexión y socket cerrados exitosamente!")