import socket
import struct
import random
import CongestionControl as cc
from slidingWindowCC import SlidingWindowCC
from socket_udp import SocketUDP

class SocketTCP:
    # Modo debug para congestion control
    DEBUG_CC = True
    
    def __init__(self):
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
        self.num_max_secuencia = 256
        self.congestion_controler = cc.CongestionControl(8)
        self.number_of_sent_segments = 0


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
                msg_recibido, nueva_direccion_servidor = self.socket_udp.recvfrom(4056)
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
            msg_recibido, direccion_cliente = self.socket_udp.recvfrom(4056)
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
                        msg_ack, _ = nuevo_socket.socket_udp.recvfrom(4056)
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
                msg_ack, _ = self.socket_udp.recvfrom(4056)
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


    def send(self, message, mode="stop_and_wait"):
        if mode == "stop_and_wait":
            self.send_using_stop_and_wait(message)
            
        else:
            self.send_using_go_back_n(message)
    

    def _recibir_confiable(self):
        self.socket_udp.settimeout(None)
        
        while True:
            msg_recibido, addr = self.socket_udp.recvfrom(4056)
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


    def recv(self, buff_size, mode="stop_and_wait"):
        if mode == "stop_and_wait":
            return self.recv_using_stop_and_wait(buff_size)

        else:
            return self.recv_using_go_back_n(buff_size)


    def close(self):
        """
        Implementa el cierre desde el lado de "Host A" tolerando pérdidas.
        Espera los paquetes ACK y FIN correspondientes retransmitiendo si es necesario.
        """
        print("\n[Close - Host A] Iniciando cierre de conexión...")
        segmento_fin = self.create_segment(b"", self.seq_num_a_enviar, syn=0, ack=0, fin=1)
        self.socket_udp.settimeout(self.TIMEOUT)      
        ack_recibido, fin_recibido = False
        intentos = 0
        direccion_b = self.direccion_destino
        ultimo_seq_b = 0
        
        self.socket_udp.sendto(segmento_fin, self.direccion_destino)
    
        while intentos < 3 and (not ack_recibido or not fin_recibido):
            try:
                msg_recibido, addr = self.socket_udp.recvfrom(4056)
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
        
        self.socket_udp.settimeout(None)

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
            msg_recibido, addr = self.socket_udp.recvfrom(4056)
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
                msg_recibido, _ = self.socket_udp.recvfrom(4056)
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

    
    def send_using_stop_and_wait(self, message):
        """Divide el mensaje en fragmentos y los envía confiablemente."""
        # Envia el primer paquete especial, el largo total del mensaje
        largo_msg_bytes = str(len(message)).encode('utf-8')
        print(f"[Send] Avisando al receptor que se enviarán {len(message)} bytes.")
        self._enviar_confiable(largo_msg_bytes)
        
        # Envia el mensaje real en trozos de máximo 16 bytes
        for i in range(0, len(message), self.MAX_PAYLOAD):
            trozo = message[i:i+self.MAX_PAYLOAD]
            self._enviar_confiable(trozo)


    def recv_using_stop_and_wait(self, buff_size):
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


    def send_using_go_back_n(self, message):
        """Envía un mensaje completo usando Go-Back-N"""
        print(f"[Send GBN] Preparando envío de {len(message)} bytes totales.")
        self.number_of_sent_segments = 0
    
        # 1. Preparar los datos a enviar
        data_list = []
        largo_msg_bytes = str(len(message)).encode('utf-8')
        data_list.append(largo_msg_bytes)
        
        # Obtener MSS
        mss = self.congestion_controler.MSS
        for i in range(0, len(message), mss):
            data_list.append(message[i:i+mss])
            
        # 2. Inicializar parametros de GBN usando congestion controller
        raw_ws = int(self.congestion_controler.get_MSS_in_cwnd())
        window_size = max(1, min(raw_ws, self.num_max_secuencia - 1))
        window = SlidingWindowCC(window_size, data_list, self.seq_num_a_enviar)

        # Debug: mostrar estado
        if self.DEBUG_CC:
            print(f"[CC Debug]")
            print(f"  MSS: {mss} bytes")
            print(f"  cwnd: {self.congestion_controler.get_cwnd()} bytes")
            print(f"  window_size: {window_size} MSSs")
            print(f"  state: {self.congestion_controler.current_state}")
            print(f"  ssthresh: {self.congestion_controler.ssthresh}")
            print()
        
        self.socket_udp.settimeout(self.TIMEOUT)
        
        base = 0  # indice del primer paquete no confirmado
        next_to_send = 0  # indice del siguiente paquete a enviar
        total_packets = len(data_list)
        initial_seq = self.seq_num_a_enviar
        dup_ack_count = 0
        last_ack_seq = None

        # 3. Ciclo principal de GBN
        while base < total_packets:
            
            # 3.1 ENVIAR paquetes hasta llenar la ventana
            while next_to_send < base + window_size and next_to_send < total_packets:
                data = window.get_data(next_to_send - base)
                seq = (self.seq_num_a_enviar + next_to_send) % self.num_max_secuencia
                segmento = self.create_segment(data, seq, syn=0, ack=0, fin=0)
                
                # Enviar con un timer (reiniciado cada envío)
                self.socket_udp.sendto(segmento, self.direccion_destino)
                self.number_of_sent_segments += 1
                next_to_send += 1
            
            try:
                # 3.2 ESPERAR ACK
                msg_ack, _ = self.socket_udp.recvfrom(4056)
                ack_segmento = self.parse_segment(msg_ack)
                
                # Mitigar Handshake retrasado
                if ack_segmento['syn'] == 1 and ack_segmento['ack'] == 1:
                    ack_seg = self.create_segment(b"", ack_segmento['seq_num'], syn=0, ack=1, fin=0)
                    self.socket_udp.sendto(ack_seg, self.direccion_destino)
                    continue
                
                # Procesar ACK acumulativo (ACK indica el siguiente seq esperado)
                if ack_segmento['ack'] == 1 and ack_segmento['syn'] == 0:
                    ack_seq = ack_segmento['seq_num']
                    base_seq = (initial_seq + base) % self.num_max_secuencia
                    ack_delta = (ack_seq - base_seq) % self.num_max_secuencia

                    # ACK duplicado o inválido
                    if ack_delta == 0 or ack_delta > (next_to_send - base):
                        continue

                    steps = ack_delta
                    window.move_window(steps)
                    base += steps

                    for _ in range(steps):
                        self.congestion_controler.event_ack_received()

                    # Ajustar ventana según cwnd
                    new_window_size = int(self.congestion_controler.get_MSS_in_cwnd())
                    if new_window_size < 1:
                        new_window_size = 1
                    if new_window_size >= self.num_max_secuencia:
                        new_window_size = self.num_max_secuencia - 1
                    if new_window_size != window_size:
                        window_size = new_window_size
                        window.update_window_size(window_size)
                                     
            except (socket.timeout, TimeoutError):
                # 3.3 TIMEOUT: Retransmitir TODOS los paquetes desde la base (GBN puro)
                print(f"\n[GBN] ¡Timeout! Retransmitiendo desde paquete {base}...")
                
                # Evento timeout en congestion controller
                self.congestion_controler.event_timeout()
                
                # Actualizar window_size después de event_timeout() (cwnd se reduce)
                old_window_size = window_size
                window_size = int(self.congestion_controler.get_MSS_in_cwnd())
                if window_size < 1:
                    window_size = 1
                if window_size >= self.num_max_secuencia:
                    window_size = self.num_max_secuencia - 1
                if window_size != old_window_size:
                    window.update_window_size(window_size)
                
                # Debug: mostrar cambio en el CC y de la ventana
                if self.DEBUG_CC:
                    print(f"[CC Debug] TIMEOUT")
                    print(f"  base: {base}, next_to_send: {next_to_send}, total: {total_packets}")
                    print(f"  cwnd: {self.congestion_controler.get_cwnd()} bytes")
                    print(f"  window_size: {window_size} MSSs (anterior: {old_window_size})")
                    print(f"  state: {self.congestion_controler.current_state}")
                    print(f"  ssthresh: {self.congestion_controler.ssthresh}")
                    print(f"  ventana interior: {list(range(base, min(base + window_size, total_packets)))}")
                    print()
                
                # Resetear el timer para poder reutilizarlo
                try:
                    if hasattr(self.socket_udp, 'timer_list') and self.socket_udp.timer_list[0] is not None:
                        self.socket_udp.stop_timer(0)
                except:
                    pass
                
                next_to_send = base
        
        # Desactivar timeout
        self.socket_udp.settimeout(None)
        
        # Actualizar secuencia global
        self.seq_num_a_enviar = (self.seq_num_a_enviar + total_packets) % self.num_max_secuencia


    def _recv_gbn(self):
        """Versión de recepción confiable que usa la lógica de secuencias de GBN"""
        # Desactivamos el timeout para quedarnos bloqueados esperando
        self.socket_udp.settimeout(None)
        
        while True:
            msg_recibido, addr = self.socket_udp.recvfrom(4056)
            segmento = self.parse_segment(msg_recibido)
                
            if segmento['syn'] == 0 and segmento['ack'] == 0:
                if segmento['seq_num'] == self.seq_num_esperado:
                    
                    # Incrementar al siguiente número de secuencia (con aritmética modular)
                    self.seq_num_esperado = (self.seq_num_esperado + 1) % self.num_max_secuencia
                    
                    # Enviar ACK confirmando el próximo paquete que esperamos
                    ack_seg = self.create_segment(b"", self.seq_num_esperado, syn=0, ack=1, fin=0)
                    self.socket_udp.sendto(ack_seg, addr)
                    
                    return segmento['data']

                else:
                    # Si llega fuera de orden, descartarlo y reenviar 
                    # el ACK del último paquete recibido (self.seq_num_esperado).
                    ack_seg = self.create_segment(b"", self.seq_num_esperado, syn=0, ack=1, fin=0)
                    self.socket_udp.sendto(ack_seg, addr)


    def recv_using_go_back_n(self, buff_size):
        """Acumula los paquetes recibidos usando Go-Back-N y entrega la cantidad solicitada."""
        # Si ya completamos un mensaje, retornar lo que queda en el buffer
        if self.bytes_esperados == 0:
            if len(self.buffer_recepcion) > 0:
                # Tenemos datos en el buffer de mensajes anteriores
                datos_retorno = self.buffer_recepcion[:buff_size]
                self.buffer_recepcion = self.buffer_recepcion[buff_size:]
                return datos_retorno
            else:
                data_largo = self._recv_gbn()
                self.bytes_esperados = int(data_largo.decode('utf-8'))
                print(f"[Recv GBN] Se espera recibir un mensaje de {self.bytes_esperados} bytes.")
            
        bytes_a_entregar_ahora = min(self.bytes_esperados, buff_size)
        
        while len(self.buffer_recepcion) < bytes_a_entregar_ahora:
            data = self._recv_gbn()
            self.buffer_recepcion += data
            
        datos_retorno = self.buffer_recepcion[:bytes_a_entregar_ahora]
        
        # Guardamos el sobrante en el buffer interno
        self.buffer_recepcion = self.buffer_recepcion[bytes_a_entregar_ahora:]
        self.bytes_esperados -= len(datos_retorno)       
        
        return datos_retorno