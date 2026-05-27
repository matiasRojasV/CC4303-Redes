# Test sin perdidas
## Cliente
python3 cliente.py 
CLIENTE - Go-Back-N
Conectado a 192.168.1.109:8000

[Test 1] Enviando mensaje de 16 bytes...
  Mensaje: b'Mensje de len=16'
[Send GBN] Preparando envío de 16 bytes totales.
  ✓ Enviado

[Test 2] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
  ✓ Enviado

[Test 3] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
  ✓ Enviado

[Cierre] Cerrando conexión...

[Close - Host A] Iniciando cierre de conexión...
[Close - Host A] ACK recibido de Host B.
[Close - Host A] FIN recibido de Host B.
[Close - Host A] ¡Respuestas recibidas con éxito! Mitigando pérdidas del último ACK...
[Close - Host A] ACK final enviado (1/3). Esperando un timeout...
[Close - Host A] ACK final enviado (2/3). Esperando un timeout...
[Close - Host A] ACK final enviado (3/3). Esperando un timeout...
[Close - Host A] ¡Conexión y recursos liberados exitosamente!
CLIENTE FINALIZADO



## Server
python3 server.py 
SERVIDOR - Go-Back-N
[SocketTCP] Escuchando (bind) en ('192.168.1.109', 8000)
Servidor escuchando en 192.168.1.109:8000...

[SocketTCP] Escuchando (bind) en ('192.168.1.109', 0)
Cliente conectado desde ('192.168.1.109', 0)

[Test 1] Recibiendo mensaje de 16 bytes...
[Recv GBN] Se espera recibir un mensaje de 16 bytes.
  Recibido: b'Mensje de len=16'
  ✓ Test 1: PASSED

[Test 2] Recibiendo mensaje de 19 bytes...
[Recv GBN] Se espera recibir un mensaje de 19 bytes.
  Recibido: b'Mensaje de largo 19'
  ✓ Test 2: PASSED

[Test 3] Recibiendo mensaje de 19 bytes en dos llamadas...
  Primera lectura (buff_size=14)...
[Recv GBN] Se espera recibir un mensaje de 19 bytes.
    Parte 1: b'Mensaje de lar' (len=14)
  Segunda lectura (buff_size=14)...
    Parte 2: b'go 19' (len=5)
  Mensaje completo: b'Mensaje de largo 19'
  ✓ Test 3: PASSED

[Cierre] Esperando cierre del cliente...

[Recv Close - Host B] Esperando petición de cierre (FIN)...
[Recv Close - Host B] FIN recibido. Enviando ACK...
[Recv Close - Host B] Enviando FIN al Host A...
[Recv Close - Host B] ACK final recibido con éxito.
[Recv Close - Host B] ¡Conexión y socket cerrados exitosamente!
SERVIDOR FINALIZADO


# Test con perdidas 20%
## cliente
python3 cliente.py 
CLIENTE - Go-Back-N
Conectado a 192.168.1.109:8000

[Test 1] Enviando mensaje de 16 bytes...
  Mensaje: b'Mensje de len=16'
[Send GBN] Preparando envío de 16 bytes totales.
  ✓ Enviado

[Test 2] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
  ✓ Enviado

[Test 3] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
  ✓ Enviado

[Cierre] Cerrando conexión...

[Close - Host A] Iniciando cierre de conexión...
[Close - Host A] ACK recibido de Host B.
[Close - Host A] FIN recibido de Host B.
[Close - Host A] ¡Respuestas recibidas con éxito! Mitigando pérdidas del último ACK...
[Close - Host A] ACK final enviado (1/3). Esperando un timeout...
[Close - Host A] ACK final enviado (2/3). Esperando un timeout...
[Close - Host A] ACK final enviado (3/3). Esperando un timeout...
[Close - Host A] ¡Conexión y recursos liberados exitosamente!
CLIENTE FINALIZADO


## server
python3 server.py 
SERVIDOR - Go-Back-N
[SocketTCP] Escuchando (bind) en ('192.168.1.109', 8000)
Servidor escuchando en 192.168.1.109:8000...

[SocketTCP] Escuchando (bind) en ('192.168.1.109', 0)
Cliente conectado desde ('192.168.1.109', 0)

[Test 1] Recibiendo mensaje de 16 bytes...
[Recv GBN] Se espera recibir un mensaje de 16 bytes.
  Recibido: b'Mensje de len=16'
  ✓ Test 1: PASSED

[Test 2] Recibiendo mensaje de 19 bytes...
[Recv GBN] Se espera recibir un mensaje de 19 bytes.
  Recibido: b'Mensaje de largo 19'
  ✓ Test 2: PASSED

[Test 3] Recibiendo mensaje de 19 bytes en dos llamadas...
  Primera lectura (buff_size=14)...
[Recv GBN] Se espera recibir un mensaje de 19 bytes.
    Parte 1: b'Mensaje de lar' (len=14)
  Segunda lectura (buff_size=14)...
    Parte 2: b'go 19' (len=5)
  Mensaje completo: b'Mensaje de largo 19'
  ✓ Test 3: PASSED

[Cierre] Esperando cierre del cliente...

[Recv Close - Host B] Esperando petición de cierre (FIN)...
[Recv Close - Host B] FIN recibido. Enviando ACK...
[Recv Close - Host B] Enviando FIN al Host A...
[Recv Close - Host B] ACK final recibido con éxito.
[Recv Close - Host B] ¡Conexión y socket cerrados exitosamente!
SERVIDOR FINALIZADO


# Test sin perdidas con cc (debug)
## cliente
python3 cliente.py 
[Send GBN] Preparando envío de 16 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 8 bytes
  window_size: 1 MSSs
  state: slow start
  ssthresh: None

[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 32 bytes
  window_size: 4 MSSs
  state: slow start
  ssthresh: None

[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 64 bytes
  window_size: 8 MSSs
  state: slow start
  ssthresh: None

[Send GBN] Preparando envío de 256 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 96 bytes
  window_size: 12 MSSs
  state: slow start
  ssthresh: None

  
## server:
 python3 server.py 
[SocketTCP] Escuchando (bind) en ('192.168.1.109', 8000)
[SocketTCP] Escuchando (bind) en ('192.168.1.109', 0)
[Recv GBN] Se espera recibir un mensaje de 16 bytes.
Test 1 received: b'Mensje de len=16'
Test 1: Passed

[Recv GBN] Se espera recibir un mensaje de 19 bytes.
Test 2 received: b'Mensaje de largo 19'
Test 2: Passed

[Recv GBN] Se espera recibir un mensaje de 19 bytes.
Test 3 received: b'Mensaje de largo 19'
Test 3: Passed

Test 4: Edge case - delaying ACKs...
[Recv GBN] Se espera recibir un mensaje de 256 bytes.
Test 4 received bytes: 256
Test 4: Passed



# Test con perdidas(20%) con cc (debug)
(sudo tc qdisc add dev lo root netem loss 20 delay 1)

## cliente
python3 cliente.py 
[Send GBN] Preparando envío de 16 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 8 bytes
  window_size: 1 MSSs
  state: slow start
  ssthresh: None


[GBN] ¡Timeout! Retransmitiendo desde paquete 1...
[CC Debug] TIMEOUT
  base: 1, next_to_send: 3, total: 3
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 8
  ventana interior: [1]


[GBN] ¡Timeout! Retransmitiendo desde paquete 2...
[CC Debug] TIMEOUT
  base: 2, next_to_send: 3, total: 3
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 8
  ventana interior: [2]

[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 16 bytes
  window_size: 2 MSSs
  state: congestion avoidance
  ssthresh: 8


[GBN] ¡Timeout! Retransmitiendo desde paquete 0...
[CC Debug] TIMEOUT
  base: 0, next_to_send: 2, total: 4
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 8
  ventana interior: [0]


[GBN] ¡Timeout! Retransmitiendo desde paquete 3...
[CC Debug] TIMEOUT
  base: 3, next_to_send: 4, total: 4
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 3)
  state: slow start
  ssthresh: 12.0
  ventana interior: [3]

[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 16 bytes
  window_size: 2 MSSs
  state: congestion avoidance
  ssthresh: 12.0


[GBN] ¡Timeout! Retransmitiendo desde paquete 0...
[CC Debug] TIMEOUT
  base: 0, next_to_send: 2, total: 4
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 8
  ventana interior: [0]


[GBN] ¡Timeout! Retransmitiendo desde paquete 0...
[CC Debug] TIMEOUT
  base: 0, next_to_send: 1, total: 4
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 1)
  state: slow start
  ssthresh: 4
  ventana interior: [0]


[GBN] ¡Timeout! Retransmitiendo desde paquete 0...
[CC Debug] TIMEOUT
  base: 0, next_to_send: 1, total: 4
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 1)
  state: slow start
  ssthresh: 4
  ventana interior: [0]


[GBN] ¡Timeout! Retransmitiendo desde paquete 3...
[CC Debug] TIMEOUT
  base: 3, next_to_send: 4, total: 4
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 3)
  state: slow start
  ssthresh: 12.0
  ventana interior: [3]

[Send GBN] Preparando envío de 256 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 16 bytes
  window_size: 2 MSSs
  state: congestion avoidance
  ssthresh: 12.0


[GBN] ¡Timeout! Retransmitiendo desde paquete 6...
[CC Debug] TIMEOUT
  base: 6, next_to_send: 10, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 4)
  state: slow start
  ssthresh: 17.0
  ventana interior: [6]


[GBN] ¡Timeout! Retransmitiendo desde paquete 9...
[CC Debug] TIMEOUT
  base: 9, next_to_send: 12, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 3)
  state: slow start
  ssthresh: 13.0
  ventana interior: [9]


[GBN] ¡Timeout! Retransmitiendo desde paquete 11...
[CC Debug] TIMEOUT
  base: 11, next_to_send: 13, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 10.0
  ventana interior: [11]


[GBN] ¡Timeout! Retransmitiendo desde paquete 11...
[CC Debug] TIMEOUT
  base: 11, next_to_send: 12, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 1)
  state: slow start
  ssthresh: 4
  ventana interior: [11]


[GBN] ¡Timeout! Retransmitiendo desde paquete 11...
[CC Debug] TIMEOUT
  base: 11, next_to_send: 12, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 1)
  state: slow start
  ssthresh: 4
  ventana interior: [11]


[GBN] ¡Timeout! Retransmitiendo desde paquete 20...
[CC Debug] TIMEOUT
  base: 20, next_to_send: 24, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 4)
  state: slow start
  ssthresh: 19.0
  ventana interior: [20]


[GBN] ¡Timeout! Retransmitiendo desde paquete 20...
[CC Debug] TIMEOUT
  base: 20, next_to_send: 21, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 1)
  state: slow start
  ssthresh: 4
  ventana interior: [20]


[GBN] ¡Timeout! Retransmitiendo desde paquete 22...
[CC Debug] TIMEOUT
  base: 22, next_to_send: 24, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 10.0
  ventana interior: [22]


[GBN] ¡Timeout! Retransmitiendo desde paquete 23...
[CC Debug] TIMEOUT
  base: 23, next_to_send: 25, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 8
  ventana interior: [23]


[GBN] ¡Timeout! Retransmitiendo desde paquete 26...
[CC Debug] TIMEOUT
  base: 26, next_to_send: 29, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 3)
  state: slow start
  ssthresh: 12.0
  ventana interior: [26]


[GBN] ¡Timeout! Retransmitiendo desde paquete 31...
[CC Debug] TIMEOUT
  base: 31, next_to_send: 33, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 3)
  state: slow start
  ssthresh: 14.0
  ventana interior: [31]


[GBN] ¡Timeout! Retransmitiendo desde paquete 32...
[CC Debug] TIMEOUT
  base: 32, next_to_send: 33, total: 33
  cwnd: 8 bytes
  window_size: 1 MSSs (anterior: 2)
  state: slow start
  ssthresh: 8
  ventana interior: [32]

## server

python3 server.py 
[SocketTCP] Escuchando (bind) en ('192.168.1.109', 8000)
[SocketTCP] Escuchando (bind) en ('192.168.1.109', 0)
[Recv GBN] Se espera recibir un mensaje de 16 bytes.
Test 1 received: b'Mensje de len=16'
Test 1: Passed

[Recv GBN] Se espera recibir un mensaje de 19 bytes.
Test 2 received: b'Mensaje de largo 19'
Test 2: Passed

[Recv GBN] Se espera recibir un mensaje de 19 bytes.
Test 3 received: b'Mensaje de largo 19'
Test 3: Passed

Test 4: Edge case - delaying ACKs...
[Recv GBN] Se espera recibir un mensaje de 256 bytes.
Test 4 received bytes: 256
Test 4: Passed
