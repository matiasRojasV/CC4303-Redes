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
python3 cliente.py 
CLIENTE - Go-Back-N
Conectado a 192.168.1.109:8000

[Test 1] Enviando mensaje de 16 bytes...
  Mensaje: b'Mensje de len=16'
[Send GBN] Preparando envío de 16 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 8 bytes
  window_size: 1 MSSs
  state: slow start
  ssthresh: None

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 16 bytes
  window_size: 2 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 24 bytes
  window_size: 3 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 32 bytes
  window_size: 4 MSSs
  state: slow start

  ✓ Enviado

[Test 2] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 32 bytes
  window_size: 4 MSSs
  state: slow start
  ssthresh: None

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 40 bytes
  window_size: 5 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 48 bytes
  window_size: 6 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 56 bytes
  window_size: 7 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 64 bytes
  window_size: 8 MSSs
  state: slow start

  ✓ Enviado

[Test 3] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 64 bytes
  window_size: 8 MSSs
  state: slow start
  ssthresh: None

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 72 bytes
  window_size: 9 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 80 bytes
  window_size: 10 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 88 bytes
  window_size: 11 MSSs
  state: slow start

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 96 bytes
  window_size: 12 MSSs
  state: slow start

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






# Test con perdidas con cc (debug)
( sudo tc qdisc add dev lo root netem loss 20 delay 3)
python3 cliente.py 
CLIENTE - Go-Back-N
Conectado a 192.168.1.109:8000

[Test 1] Enviando mensaje de 16 bytes...
  Mensaje: b'Mensje de len=16'
[Send GBN] Preparando envío de 16 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 8 bytes
  window_size: 1 MSSs
  state: slow start
  ssthresh: None


[GBN] ¡Timeout! Retransmitiendo desde paquete 0...
[CC Debug] TIMEOUT
  cwnd: 8 bytes
  window_size: 1 MSSs
  state: slow start
  ssthresh: 4

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 16 bytes
  window_size: 2 MSSs
  state: congestion avoidance

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 20.0 bytes
  window_size: 2.0 MSSs
  state: congestion avoidance

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 24.0 bytes
  window_size: 3.0 MSSs
  state: congestion avoidance

  ✓ Enviado

[Test 2] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 24.0 bytes
  window_size: 3 MSSs
  state: congestion avoidance
  ssthresh: 4


[GBN] ¡Timeout! Retransmitiendo desde paquete 0...
[CC Debug] TIMEOUT
  cwnd: 8 bytes
  window_size: 1 MSSs
  state: slow start
  ssthresh: 12.0

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 16 bytes
  window_size: 2 MSSs
  state: congestion avoidance

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 20.0 bytes
  window_size: 2.0 MSSs
  state: congestion avoidance

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 24.0 bytes
  window_size: 3.0 MSSs
  state: congestion avoidance

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 26.666666666666668 bytes
  window_size: 3.0 MSSs
  state: congestion avoidance

  ✓ Enviado

[Test 3] Enviando mensaje de 19 bytes...
  Mensaje: b'Mensaje de largo 19'
[Send GBN] Preparando envío de 19 bytes totales.
[CC Debug]
  MSS: 8 bytes
  cwnd: 26.666666666666668 bytes
  window_size: 3 MSSs
  state: congestion avoidance
  ssthresh: 12.0

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 29.333333333333336 bytes
  window_size: 3.0 MSSs
  state: congestion avoidance

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 32.0 bytes
  window_size: 4.0 MSSs
  state: congestion avoidance


[GBN] ¡Timeout! Retransmitiendo desde paquete 2...
[CC Debug] TIMEOUT
  cwnd: 8 bytes
  window_size: 1 MSSs
  state: slow start
  ssthresh: 16.0

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 16 bytes
  window_size: 2 MSSs
  state: congestion avoidance

[CC Debug] ACK recibido (1 paquetes confirmados)
  cwnd: 20.0 bytes
  window_size: 2.0 MSSs
  state: congestion avoidance

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
